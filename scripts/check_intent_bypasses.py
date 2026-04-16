"""
CI/CD script to detect intent classification bypasses.
Run this in CI to fail builds if bypasses detected.
"""

import re
import sys
from pathlib import Path


def check_bypasses():
    """Scan for potential intent bypasses."""

    bypasses = []

    # Check web routes
    web_files = Path("web").glob("**/*.py")
    for file in web_files:
        content = file.read_text()

        # Find route definitions
        routes = re.findall(r'@(?:app|router)\.(get|post|put|delete)\(["\']([^"\']+)', content)

        for method, path in routes:
            # Skip exempt paths
            if any(
                exempt in path
                for exempt in ["/health", "/metrics", "/docs", "/static", "/api/v1/personality"]
            ):
                continue

            # Check if looks like NL but not in middleware
            if any(
                keyword in path.lower() for keyword in ["chat", "message", "talk", "ask", "query"]
            ):
                # Check if endpoint uses intent
                route_start = content.find(f"@{method}")
                next_500 = content[route_start : route_start + 500]

                if "intent" not in next_500.lower():
                    bypasses.append(
                        {
                            "file": str(file),
                            "method": method.upper(),
                            "path": path,
                            "reason": "NL-like endpoint without intent usage",
                        }
                    )

    return bypasses


if __name__ == "__main__":
    bypasses = check_bypasses()

    if bypasses:
        print(f"❌ FOUND {len(bypasses)} POTENTIAL BYPASSES:")
        for b in bypasses:
            print(f"  {b['method']:6} {b['path']:40} ({b['file']})")
            print(f"         Reason: {b['reason']}")
        sys.exit(1)
    else:
        print("✅ NO BYPASSES DETECTED")
        sys.exit(0)
