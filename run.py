"""Interactive CLI for the shopping assistant."""
import sys
from pathlib import Path

# Ensure project root is in sys.path
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from app.main import create_agent


def main() -> None:
    agent = create_agent()
    print("=====================================")
    print("Scalable Agentic Shopping Assistant")
    print("=====================================")
    while True:
        query = input("\nEnter your question: ").strip()
        if query.lower() in {"exit", "quit"}: break
        state = agent.invoke("C001", query)
        print(f"\nDetected domain: {state.get('domain')}\nDetected intent: {state.get('intent')}")
        print(f"Total registered tools: {len(agent.registry)}")
        print(f"Tools exposed to agent: {len(state.get('selected_tools', []))}")
        print(f"Selected tools: {', '.join(state.get('completed_steps', []))}")
        print(f"\nFinal answer: {state.get('final_response')}")


if __name__ == "__main__": main()
