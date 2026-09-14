from backend.app.agents.core.tool_router import execute_tool

print(execute_tool("dashboard"))

print("=" * 50)

print(execute_tool("forecast"))

print("=" * 50)

print(execute_tool("system_health"))

print("=" * 50)
print(execute_tool("history"))

print(execute_tool("optimization"))