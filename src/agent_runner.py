#!/usr/bin/env python3
"""
CoralCloud Agent Runner
Orchestrates AI agents using Claude API with lightweight Python.
"""

import os
import sys
import yaml
import anthropic
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import csv
import glob


class AgentRunner:
    """Main orchestrator for CoralCloud AI agents"""

    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.repo_root = Path(__file__).parent.parent
        self.config_path = self.repo_root / "agents" / agent_name / "config.yaml"
        self.config = self._load_config()
        self.client = self._init_claude_client()

    def _load_config(self) -> Dict[str, Any]:
        """Load agent configuration from YAML"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config not found: {self.config_path}")

        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def _init_claude_client(self) -> anthropic.Anthropic:
        """Initialize Claude API client"""
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        return anthropic.Anthropic(api_key=api_key)

    def _read_input_files(self) -> Dict[str, str]:
        """Read all input files specified in config"""
        inputs = {}

        for source in self.config.get('inputs', {}).get('data_sources', []):
            path = source['path']
            input_type = source['type']

            # Handle glob patterns
            if '*' in path:
                files = glob.glob(str(self.repo_root / path))
                for file_path in files:
                    file_key = Path(file_path).stem
                    inputs[file_key] = self._read_file(file_path, input_type)
            else:
                file_path = self.repo_root / path
                if file_path.exists():
                    inputs[path] = self._read_file(str(file_path), input_type)

        # Read context files
        for context_file in self.config.get('inputs', {}).get('context_files', []):
            if '*' in context_file:
                files = glob.glob(str(self.repo_root / context_file))
                for file_path in files:
                    file_key = Path(file_path).stem
                    inputs[file_key] = self._read_file(file_path, 'text')
            else:
                file_path = self.repo_root / context_file
                if file_path.exists():
                    inputs[context_file] = self._read_file(str(file_path), 'text')

        return inputs

    def _read_file(self, file_path: str, file_type: str) -> str:
        """Read a single file and return its contents"""
        path = Path(file_path)

        if not path.exists():
            return f"[File not found: {file_path}]"

        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            if file_type == 'csv':
                return f"CSV Content from {path.name}:\n{content}"
            elif file_type == 'markdown':
                return f"Markdown from {path.name}:\n{content}"
            else:
                return content
        except Exception as e:
            return f"[Error reading {file_path}: {str(e)}]"

    def _build_prompt(self, prompt_key: str, **kwargs) -> str:
        """Build prompt from config with variable substitution"""
        prompt_template = self.config.get('prompts', {}).get(prompt_key, '')

        # Add date variables
        now = datetime.now()
        kwargs['date'] = now.strftime('%Y-%m-%d')
        kwargs['quarter'] = f"{(now.month - 1) // 3 + 1}"
        kwargs['day_of_week'] = now.strftime('%A')

        # Add placeholders for optional variables if not provided
        if 'recent_context' not in kwargs:
            kwargs['recent_context'] = "No recent context available"
        if 'opportunity_description' not in kwargs:
            kwargs['opportunity_description'] = ""
        if 'client_name' not in kwargs:
            kwargs['client_name'] = ""
        if 'source' not in kwargs:
            kwargs['source'] = ""
        if 'requirements' not in kwargs:
            kwargs['requirements'] = ""
        if 'topic' not in kwargs:
            kwargs['topic'] = ""
        if 'asset_type' not in kwargs:
            kwargs['asset_type'] = ""
        if 'audience' not in kwargs:
            kwargs['audience'] = ""
        if 'use_case' not in kwargs:
            kwargs['use_case'] = ""

        return prompt_template.format(**kwargs)

    def _call_claude(self, system_prompt: str, user_prompt: str) -> str:
        """Make API call to Claude"""
        claude_config = self.config.get('claude_config', {})

        try:
            message = self.client.messages.create(
                model=claude_config.get('model', 'claude-3-5-sonnet-20241022'),
                max_tokens=claude_config.get('max_tokens', 4096),
                temperature=claude_config.get('temperature', 0.7),
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            return message.content[0].text
        except Exception as e:
            raise RuntimeError(f"Claude API call failed: {str(e)}")

    def _save_output(self, content: str, output_config: Dict[str, Any]) -> Path:
        """Save agent output to file"""
        output_path = output_config['path']

        # Replace date placeholder
        output_path = output_path.replace('{date}', datetime.now().strftime('%Y-%m-%d'))

        full_path = self.repo_root / output_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return full_path

    def run(self, prompt_key: str = None) -> Dict[str, Any]:
        """Execute the agent"""
        print(f"🚀 Running {self.config['name']} ({self.config['icon']})")
        print(f"Purpose: {self.config['purpose']}")
        print("-" * 60)

        try:
            # Read inputs
            print("📥 Reading inputs...")
            inputs = self._read_input_files()
            print(f"   Loaded {len(inputs)} input files")

            # Build prompts
            print("🧠 Building prompts...")
            system_prompt = self._build_prompt('system')

            # Determine which prompt to use
            if prompt_key is None:
                # Use the first available prompt that's not 'system'
                prompt_keys = [k for k in self.config.get('prompts', {}).keys() if k != 'system']
                prompt_key = prompt_keys[0] if prompt_keys else 'system'

            user_prompt = self._build_prompt(prompt_key)

            # Add inputs to user prompt
            inputs_text = "\n\n## Available Data:\n"
            for key, value in inputs.items():
                inputs_text += f"\n### {key}\n{value}\n"

            full_user_prompt = user_prompt + inputs_text

            # Call Claude
            print(f"💬 Calling Claude API ({self.config['claude_config']['model']})...")
            response = self._call_claude(system_prompt, full_user_prompt)

            # Save outputs
            print("💾 Saving outputs...")
            output_files = []

            primary_output = self.config['outputs']['primary']
            output_file = self._save_output(response, primary_output)
            output_files.append(output_file)
            print(f"   ✓ {output_file.relative_to(self.repo_root)}")

            print("-" * 60)
            print(f"✅ {self.config['name']} completed successfully!")

            return {
                'success': True,
                'agent': self.agent_name,
                'outputs': output_files,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return {
                'success': False,
                'agent': self.agent_name,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }


def run_strategic() -> Dict[str, Any]:
    """Run the Strategic Agent (AI Co-Founder)"""
    runner = AgentRunner('strategic')
    return runner.run('weekly_report')


def run_growth() -> Dict[str, Any]:
    """Run the Growth Agent (Marketing/LinkedIn)"""
    runner = AgentRunner('growth')
    return runner.run('daily_post')


def run_finance() -> Dict[str, Any]:
    """Run the Finance & Compliance Agent"""
    runner = AgentRunner('finance')
    return runner.run('weekly_summary')


def run_business() -> Dict[str, Any]:
    """Run the Business Agent (Income/Consulting)"""
    runner = AgentRunner('business')
    return runner.run('daily_pipeline')


def run_retail() -> Dict[str, Any]:
    """Run the Retail Intelligence Agent (SAP/CAR)"""
    runner = AgentRunner('retail')
    return runner.run('biweekly_review')


def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: python agent_runner.py <agent_name>")
        print("Available agents: strategic, growth, finance, business, retail")
        sys.exit(1)

    agent_name = sys.argv[1].lower()

    agent_functions = {
        'strategic': run_strategic,
        'growth': run_growth,
        'finance': run_finance,
        'business': run_business,
        'retail': run_retail
    }

    if agent_name not in agent_functions:
        print(f"Unknown agent: {agent_name}")
        print(f"Available: {', '.join(agent_functions.keys())}")
        sys.exit(1)

    result = agent_functions[agent_name]()

    if not result['success']:
        sys.exit(1)


if __name__ == '__main__':
    main()
