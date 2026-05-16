import { useEffect, useState } from "react";
import "./App.css";

type Topic = {
  topic: string;
  minutes: number;
};

type ActivityBlock = {
  start: string;
  end: string;
  topic: string;
  category: string;
  duration_minutes: number;
  evidence: string[];
};

type DailySummary = {
  date: string;
  total_tracked_minutes: number;
  total_sessions: number;
  top_topics: Topic[];
  major_activity_blocks: ActivityBlock[];
};

type WeeklyReview = {
  date: string;
  review_window_days: number;
  active_tracked_days: number;
  total_summarized_minutes: number;
  top_weekly_topics: Topic[];
  recurring_themes: string[];
};

type Tab = "today" | "weekly" | "ai";

type AIRecap = {
  source_file: string;
  recap: string;
};

function App() {
  const [activeTab, setActiveTab] = useState<Tab>("today");
  const [summary, setSummary] = useState<DailySummary | null>(null);
  const [weekly, setWeekly] = useState<WeeklyReview | null>(null);
  const [loading, setLoading] = useState(true);
  const [aiRecap, setAiRecap] = useState<AIRecap | null>(null);

  useEffect(() => {
    Promise.all([
      fetch("http://127.0.0.1:8000/daily-summary").then((res) => res.json()),
      fetch("http://127.0.0.1:8000/weekly-review").then((res) => res.json()),
      fetch("http://127.0.0.1:8000/ai-recap").then((res) => res.json()),
    ])
    .then(([dailyData, weeklyData, aiData]) => {
      setSummary(dailyData);
      setWeekly(weeklyData);
      setAiRecap(aiData);
      setLoading(false);
    })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <main className="page">Loading Chronicle...</main>;
  }

  return (
    <main className="page">
      <section className="hero">
        <div>
          <p className="eyebrow">Local AI Workflow Memory</p>
          <h1>Chronicle</h1>
          <p className="subtitle">
            Reconstructing your work sessions, themes, and context from local activity data.
          </p>
        </div>

        <div className="status-pill">API Connected</div>
      </section>

      <nav className="tabs">
        <button
          className={activeTab === "today" ? "tab active" : "tab"}
          onClick={() => setActiveTab("today")}
        >
          Today
        </button>

        <button
          className={activeTab === "weekly" ? "tab active" : "tab"}
          onClick={() => setActiveTab("weekly")}
        >
          Weekly Review
        </button>

        <button
          className={activeTab === "ai" ? "tab active" : "tab"}
          onClick={() => setActiveTab("ai")}
        >
          AI Recap
        </button>
      </nav>

      {activeTab === "today" && summary && <TodayView summary={summary} />}
      {activeTab === "weekly" && weekly && <WeeklyView weekly={weekly} />}
      {activeTab === "ai" && <AIView aiRecap={aiRecap} />}
    </main>
  );
}

function TodayView({ summary }: { summary: DailySummary }) {
  return (
    <>
      <section className="stats-grid">
        <div className="stat-card">
          <span>Date</span>
          <strong>{summary.date}</strong>
        </div>

        <div className="stat-card">
          <span>Tracked Time</span>
          <strong>{summary.total_tracked_minutes} min</strong>
        </div>

        <div className="stat-card">
          <span>Sessions</span>
          <strong>{summary.total_sessions}</strong>
        </div>
      </section>

      <section className="content-grid">
        <div className="panel">
          <h2>Top Topics</h2>

          <div className="topic-list">
            {summary.top_topics.map((topic) => (
              <div className="topic-row" key={topic.topic}>
                <span>{topic.topic}</span>
                <strong>{topic.minutes} min</strong>
              </div>
            ))}
          </div>
        </div>

        <div className="panel">
          <h2>System Notes</h2>
          <p className="note">
            Chronicle is currently running as a local-first activity intelligence system using
            SQLite, FastAPI, React, and local AI-ready summaries.
          </p>
        </div>
      </section>

      <section className="panel">
        <h2>Major Activity Blocks</h2>

        <div className="activity-stack">
          {summary.major_activity_blocks.map((block, index) => (
            <article className="activity-card" key={index}>
              <div className="activity-header">
                <div>
                  <h3>{block.topic}</h3>
                  <p>
                    {block.start} - {block.end}
                  </p>
                </div>

                <span className="duration">{block.duration_minutes} min</span>
              </div>

              <div className="tag-row">
                <span>{block.category}</span>
              </div>

              <ul className="evidence-list">
                {block.evidence.map((item, i) => (
                  <li key={i}>{item}</li>
                ))}
              </ul>
            </article>
          ))}
        </div>
      </section>
    </>
  );
}

function WeeklyView({ weekly }: { weekly: WeeklyReview }) {
  return (
    <>
      <section className="stats-grid">
        <div className="stat-card">
          <span>Review Date</span>
          <strong>{weekly.date}</strong>
        </div>

        <div className="stat-card">
          <span>Window</span>
          <strong>{weekly.review_window_days} days</strong>
        </div>

        <div className="stat-card">
          <span>Total Time</span>
          <strong>{weekly.total_summarized_minutes} min</strong>
        </div>
      </section>

      <section className="content-grid">
        <div className="panel">
          <h2>Top Weekly Topics</h2>

          <div className="topic-list">
            {weekly.top_weekly_topics.map((topic) => (
              <div className="topic-row" key={topic.topic}>
                <span>{topic.topic}</span>
                <strong>{topic.minutes} min</strong>
              </div>
            ))}
          </div>
        </div>

        <div className="panel">
          <h2>Recurring Themes</h2>

          <div className="theme-stack">
            {weekly.recurring_themes.length > 0 ? (
              weekly.recurring_themes.map((theme) => (
                <span className="theme-pill" key={theme}>
                  {theme}
                </span>
              ))
            ) : (
              <p className="note">No recurring themes detected yet.</p>
            )}
          </div>
        </div>
      </section>
    </>
  );
}

function AIView({ aiRecap }: { aiRecap: AIRecap | null }) {
  if (!aiRecap) {
    return (
      <section className="panel">
        <h2>AI Recap</h2>
        <p className="note">
          No AI recap found yet. Run:
        </p>

        <pre className="code-block">python -m scripts.ask_chronicle</pre>
      </section>
    );
  }

  return (
    <section className="panel">
      <h2>AI Recap</h2>

      <p className="note">
        Source: {aiRecap.source_file}
      </p>

      <div className="ai-recap-box">
      <pre className="ai-recap-text">{aiRecap.recap}</pre>
      </div>
    </section>
  );
}

export default App;