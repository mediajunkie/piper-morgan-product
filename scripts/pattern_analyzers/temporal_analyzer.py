"""
Temporal Analysis - Velocity tracking and work intensity patterns.

Detects:
- Commit velocity changes via GitPython
- Velocity spikes (>50% change from baseline)
- Work intensity clustering (intensive periods)
- Parallel agent work from session log timestamps
- Issue closure rate changes
"""

import re
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from git import Repo

from .base import BaseAnalyzer, BreakthroughSignal


class TemporalAnalyzer(BaseAnalyzer):
    """
    Analyzes temporal patterns in development velocity and coordination.

    Uses GitPython to track commit patterns and session logs to detect
    parallel work and coordination effectiveness.
    """

    def __init__(self, project_root: Path):
        super().__init__(project_root)
        self.repo = Repo(project_root)
        self.session_logs_dir = project_root / "dev" / "2025"

    async def analyze(
        self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Run temporal analysis for specified time period.

        Returns:
            Dict with keys:
            - velocity_data: Commit velocity over time
            - velocity_spikes: Detected velocity anomalies
            - parallel_work: Concurrent agent sessions
            - work_clusters: Intensive work periods
            - issue_closures: Issue completion rate
        """
        if end_date is None:
            end_date = datetime.now()
        if start_date is None:
            # Default to last 30 days
            start_date = end_date - timedelta(days=30)

        # Analyze git commit velocity
        velocity_data = self._analyze_commit_velocity(start_date, end_date)

        # Detect velocity spikes
        velocity_spikes = self._detect_velocity_spikes(velocity_data)

        # Analyze session log timing for parallel work
        parallel_work = self._analyze_parallel_sessions(start_date, end_date)

        # Identify work intensity clusters
        work_clusters = self._identify_work_clusters(velocity_data, parallel_work)

        # Analyze issue closure rate (from commit messages)
        issue_closures = self._analyze_issue_closures(start_date, end_date)

        self.results = {
            "velocity_data": velocity_data,
            "velocity_spikes": velocity_spikes,
            "parallel_work": parallel_work,
            "work_clusters": work_clusters,
            "issue_closures": issue_closures,
            "analysis_period": {
                "start": self._format_date(start_date),
                "end": self._format_date(end_date),
            },
        }

        return self.results

    def _analyze_commit_velocity(
        self, start_date: datetime, end_date: datetime, window_days: int = 7
    ) -> Dict[str, Any]:
        """
        Calculate commit velocity over time windows.

        Args:
            start_date: Start of analysis period
            end_date: End of analysis period
            window_days: Size of rolling window for velocity calculation

        Returns:
            Dict with velocity measurements per time window
        """
        # Get all commits in date range
        commits_by_date = defaultdict(list)

        for commit in self.repo.iter_commits(since=start_date, until=end_date):
            commit_date = datetime.fromtimestamp(commit.committed_date).date()
            commits_by_date[commit_date].append(
                {
                    "sha": commit.hexsha[:8],
                    "message": commit.message.split("\n")[0][:100],
                    "author": commit.author.name,
                    "files_changed": len(commit.stats.files),
                }
            )

        # Calculate rolling window velocity
        velocity_windows = []
        current_date = start_date.date()

        while current_date <= end_date.date():
            window_start = current_date
            window_end = current_date + timedelta(days=window_days)

            # Count commits in this window
            window_commits = 0
            window_files = 0
            for date in commits_by_date:
                if window_start <= date < window_end:
                    window_commits += len(commits_by_date[date])
                    window_files += sum(c["files_changed"] for c in commits_by_date[date])

            velocity_windows.append(
                {
                    "window_start": str(window_start),
                    "window_end": str(window_end),
                    "commits": window_commits,
                    "files_changed": window_files,
                    "commits_per_day": window_commits / window_days if window_days > 0 else 0,
                }
            )

            current_date += timedelta(days=1)

        # Calculate baseline velocity (median)
        velocities = [w["commits_per_day"] for w in velocity_windows if w["commits_per_day"] > 0]
        baseline_velocity = sorted(velocities)[len(velocities) // 2] if velocities else 0

        return {
            "windows": velocity_windows,
            "baseline_velocity": baseline_velocity,
            "total_commits": sum(len(commits) for commits in commits_by_date.values()),
            "commits_by_date": {str(date): commits for date, commits in commits_by_date.items()},
        }

    def _detect_velocity_spikes(
        self, velocity_data: Dict[str, Any], threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Detect velocity spikes (>threshold change from baseline).

        Args:
            velocity_data: Output from _analyze_commit_velocity
            threshold: Minimum change ratio to qualify as spike (0.5 = 50%)

        Returns:
            List of detected spikes with evidence
        """
        baseline = velocity_data["baseline_velocity"]
        if baseline == 0:
            return []

        spikes = []
        for window in velocity_data["windows"]:
            velocity = window["commits_per_day"]

            if velocity > baseline * (1 + threshold):
                spike_ratio = (velocity - baseline) / baseline
                spikes.append(
                    {
                        "date": window["window_start"],
                        "velocity": velocity,
                        "baseline": baseline,
                        "spike_ratio": spike_ratio,
                        "commits": window["commits"],
                        "files_changed": window["files_changed"],
                        "severity": (
                            "high"
                            if spike_ratio > 2.0
                            else "medium"
                            if spike_ratio > 1.0
                            else "low"
                        ),
                    }
                )

        return spikes

    def _analyze_parallel_sessions(
        self, start_date: datetime, end_date: datetime
    ) -> Dict[str, Any]:
        """
        Detect parallel agent work from session log timestamps.

        Parses session log filenames (YYYY-MM-DD-HHMM-role-agent-log.md)
        to find overlapping work periods.

        Returns:
            Dict with parallel session analysis
        """
        if not self.session_logs_dir.exists():
            return {"parallel_days": [], "max_concurrent_agents": 0}

        # Parse session log files to extract timestamps and roles
        sessions_by_date = defaultdict(list)

        for month_dir in self.session_logs_dir.iterdir():
            if not month_dir.is_dir():
                continue

            for day_dir in month_dir.iterdir():
                if not day_dir.is_dir():
                    continue

                # Extract date from directory name (MM/DD/)
                try:
                    year = self.session_logs_dir.name  # "2025"
                    month = month_dir.name  # "11"
                    day = day_dir.name  # "03"
                    log_date = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")

                    if not (start_date <= log_date <= end_date):
                        continue

                    # Parse session log files in this directory
                    for log_file in day_dir.glob("*-log.md"):
                        # Filename format: YYYY-MM-DD-HHMM-role-agent-log.md
                        match = re.match(
                            r"(\d{4})-(\d{2})-(\d{2})-(\d{4})-(\w+)-(\w+)-log\.md", log_file.name
                        )

                        if match:
                            year, month, day, time, role, agent = match.groups()
                            hour = int(time[:2])
                            minute = int(time[2:])

                            session_dt = datetime(int(year), int(month), int(day), hour, minute)

                            sessions_by_date[log_date.date()].append(
                                {
                                    "timestamp": self._format_date(session_dt),
                                    "role": role,
                                    "agent": agent,
                                    "file": str(log_file),
                                }
                            )

                except (ValueError, AttributeError):
                    continue

        # Find days with parallel work (multiple sessions at overlapping times)
        parallel_days = []

        for date, sessions in sessions_by_date.items():
            if len(sessions) > 1:
                # Sort by timestamp
                sorted_sessions = sorted(sessions, key=lambda s: s["timestamp"])

                # Count max concurrent sessions (simplistic: sessions within 4 hours = concurrent)
                max_concurrent = 1
                for i, session in enumerate(sorted_sessions):
                    concurrent_count = 1
                    session_time = self._parse_date(session["timestamp"])

                    for j, other_session in enumerate(sorted_sessions):
                        if i != j:
                            other_time = self._parse_date(other_session["timestamp"])
                            # Within 4 hours = likely concurrent work
                            if abs((session_time - other_time).total_seconds()) < 4 * 3600:
                                concurrent_count += 1

                    max_concurrent = max(max_concurrent, concurrent_count)

                parallel_days.append(
                    {
                        "date": str(date),
                        "session_count": len(sessions),
                        "max_concurrent": max_concurrent,
                        "sessions": sorted_sessions,
                    }
                )

        max_concurrent_overall = (
            max(day["max_concurrent"] for day in parallel_days) if parallel_days else 0
        )

        return {
            "parallel_days": parallel_days,
            "max_concurrent_agents": max_concurrent_overall,
            "total_parallel_days": len(parallel_days),
        }

    def _identify_work_clusters(
        self, velocity_data: Dict[str, Any], parallel_work: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Identify intensive work periods (clusters of high velocity + parallel work).

        Returns:
            List of work cluster periods with characteristics
        """
        clusters = []

        # Find dates with both high velocity and parallel work
        velocity_by_date = {}
        for window in velocity_data["windows"]:
            date_str = window["window_start"]
            velocity_by_date[date_str] = window["commits_per_day"]

        parallel_dates = {day["date"] for day in parallel_work.get("parallel_days", [])}

        for date_str in velocity_by_date:
            velocity = velocity_by_date[date_str]
            baseline = velocity_data["baseline_velocity"]

            # High velocity + parallel work = intensive cluster
            if velocity > baseline * 1.5 and date_str in parallel_dates:
                parallel_info = next(
                    (d for d in parallel_work["parallel_days"] if d["date"] == date_str), None
                )

                clusters.append(
                    {
                        "date": date_str,
                        "velocity": velocity,
                        "baseline": baseline,
                        "velocity_multiplier": velocity / baseline if baseline > 0 else 0,
                        "concurrent_agents": (
                            parallel_info["max_concurrent"] if parallel_info else 0
                        ),
                        "intensity": (
                            "very_high"
                            if velocity > baseline * 2.0
                            else "high"
                            if velocity > baseline * 1.5
                            else "medium"
                        ),
                    }
                )

        return sorted(clusters, key=lambda c: c["velocity"], reverse=True)

    def _analyze_issue_closures(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """
        Analyze issue closure rate from commit messages.

        Looks for patterns like "fix #123", "closes #456" in commits.

        Returns:
            Dict with issue closure analysis
        """
        issue_pattern = re.compile(
            r"(?:fix(?:es|ed)?|close(?:s|d)?|resolve(?:s|d)?)\s+#(\d+)", re.IGNORECASE
        )

        issues_by_date = defaultdict(list)

        for commit in self.repo.iter_commits(since=start_date, until=end_date):
            matches = issue_pattern.findall(commit.message)
            if matches:
                commit_date = datetime.fromtimestamp(commit.committed_date).date()
                for issue_num in matches:
                    issues_by_date[commit_date].append(
                        {"issue": f"#{issue_num}", "commit": commit.hexsha[:8]}
                    )

        # Calculate closure velocity
        total_issues = sum(len(issues) for issues in issues_by_date.values())
        days_with_closures = len(issues_by_date)
        avg_closures_per_day = total_issues / days_with_closures if days_with_closures > 0 else 0

        # Find spike days (>2x average)
        spike_days = []
        for date, issues in issues_by_date.items():
            if len(issues) > avg_closures_per_day * 2:
                spike_days.append(
                    {
                        "date": str(date),
                        "issues_closed": len(issues),
                        "average": avg_closures_per_day,
                        "spike_ratio": (
                            len(issues) / avg_closures_per_day if avg_closures_per_day > 0 else 0
                        ),
                    }
                )

        return {
            "total_issues_closed": total_issues,
            "avg_closures_per_day": avg_closures_per_day,
            "spike_days": spike_days,
            "issues_by_date": {str(date): issues for date, issues in issues_by_date.items()},
        }

    def get_breakthrough_signals(self) -> Dict[BreakthroughSignal, Any]:
        """
        Extract breakthrough signals from temporal analysis.

        Returns:
            Dict mapping signal types to evidence
        """
        if not self.results:
            return {}

        signals = {}

        # Velocity spike signal
        velocity_spikes = self.results.get("velocity_spikes", [])
        if velocity_spikes:
            signals[BreakthroughSignal.VELOCITY_SPIKE] = {
                "count": len(velocity_spikes),
                "max_spike": max(s["spike_ratio"] for s in velocity_spikes),
                "dates": [s["date"] for s in velocity_spikes],
            }

        # Parallel work signal
        parallel_work = self.results.get("parallel_work", {})
        max_concurrent = parallel_work.get("max_concurrent_agents", 0)
        if max_concurrent >= 3:  # 3+ agents = significant parallel work
            signals[BreakthroughSignal.PARALLEL_WORK] = {
                "max_concurrent_agents": max_concurrent,
                "parallel_days": parallel_work.get("total_parallel_days", 0),
                "dates": [d["date"] for d in parallel_work.get("parallel_days", [])],
            }

        # Completion spike signal
        issue_closures = self.results.get("issue_closures", {})
        spike_days = issue_closures.get("spike_days", [])
        if spike_days:
            signals[BreakthroughSignal.COMPLETION_SPIKE] = {
                "count": len(spike_days),
                "max_closures": max(s["issues_closed"] for s in spike_days),
                "dates": [s["date"] for s in spike_days],
            }

        return signals
