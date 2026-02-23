import time
import textwrap
from django.db import connection


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Start timer and get initial query count
        start_time = time.time()
        initial_queries = len(connection.queries)

        # Process request
        response = self.get_response(request)

        # Calculate time taken and queries executed
        duration = time.time() - start_time
        final_queries = connection.queries[initial_queries:]
        num_queries = len(final_queries)

        # Prepare log information
        method = request.method
        path = request.get_full_path()
        status_code = response.status_code
        db_time = sum(float(q.get("time", 0)) for q in final_queries)

        # Build the ASCII rectangle
        try:
            res_content = (
                response.content.decode("utf-8")
                if hasattr(response, "content")
                else "[No Content]"
            )
        except Exception:
            res_content = "[Binary/Undecodable Content]"

        self.log_request_response(
            method, path, status_code, duration, num_queries, db_time, res_content
        )

        return response

    def log_request_response(
        self,
        method,
        path,
        status_code,
        duration,
        num_queries,
        db_time,
        response_content,
    ):
        box_width = 100

        lines = []
        lines.append(f"┌{'─' * (box_width - 2)}┐")

        title = " REQUEST / RESPONSE LOG "
        # Some colors for the terminal (ANSI escape codes)
        RESET = "\033[0m"
        BOLD = "\033[1m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        RED = "\033[91m"
        BLUE = "\033[94m"
        CYAN = "\033[96m"

        # Color the status code
        if 200 <= status_code < 300:
            status_color = GREEN
        elif 300 <= status_code < 400:
            status_color = CYAN
        elif 400 <= status_code < 500:
            status_color = YELLOW
        else:
            status_color = RED

        lines.append(f"│{title.center(box_width - 2)}│")
        lines.append(f"├{'─' * (box_width - 2)}┤")

        # Details
        req_info = f" Request: {BLUE}{BOLD}{method}{RESET} {path}"
        res_info = f" Response Status: {status_color}{BOLD}{status_code}{RESET}"
        time_info = f" Duration: {duration:.4f}s"
        db_info = f" DB Queries Executed: {num_queries} (Total Time: {db_time:.4f}s)"

        # Calculate visual length ignoring ansi codes
        def get_visual_len(text):
            import re

            ansi_escape = re.compile(r"(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]")
            return len(ansi_escape.sub("", text))

        def align_text(text, width):
            v_len = get_visual_len(text)
            padding = width - v_len
            return text + " " * padding

        lines.append(f"│{align_text(req_info, box_width - 2)}│")
        lines.append(f"│{align_text(res_info, box_width - 2)}│")
        lines.append(f"│{align_text(time_info, box_width - 2)}│")
        lines.append(f"│{align_text(db_info, box_width - 2)}│")

        if response_content:
            lines.append(f"├{'─' * (box_width - 2)}┤")
            # Truncate content to avoid huge logs
            truncated_content = response_content[:500] + (
                "..." if len(response_content) > 500 else ""
            )
            wrapped_content = textwrap.wrap(
                f"Response Payload: {truncated_content}", width=box_width - 4
            )
            for line in wrapped_content:
                lines.append(f"│{align_text(' ' + line, box_width - 2)}│")

        lines.append(f"└{'─' * (box_width - 2)}┘")

        output = "\n".join(lines)
        try:
            print(output)
        except UnicodeEncodeError:
            safe_output = (
                output.replace("┌", "+")
                .replace("─", "-")
                .replace("┐", "+")
                .replace("│", "|")
                .replace("├", "+")
                .replace("┤", "+")
                .replace("└", "+")
                .replace("┘", "+")
            )
            print(safe_output)
