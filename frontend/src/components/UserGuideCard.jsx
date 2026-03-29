export default function UserGuideCard() {
  return (
    <div className="card">
      <h2 className="section-title">How To Use ISMAP</h2>
      <p className="intro">
        Your dashboard is focused on scanning, tracking changes, and exporting results.
      </p>

      <div className="guide-list">
        <div className="guide-item">
          <strong>1. Register a domain</strong>
          <span>Add a domain you want ISMAP to monitor over time.</span>
        </div>
        <div className="guide-item">
          <strong>2. Run Start Scan</strong>
          <span>Launch a live scan and watch discovered subdomains stream into the table.</span>
        </div>
        <div className="guide-item">
          <strong>3. Check scan history</strong>
          <span>Review earlier scans to see what changed for that domain.</span>
        </div>
        <div className="guide-item">
          <strong>4. Export reports</strong>
          <span>Download JSON or TXT reports when you need to share findings.</span>
        </div>
      </div>

      <style>{`
        .section-title {
          margin: 0 0 0.85rem;
          font-size: 1.1rem;
          font-weight: 600;
        }
        .intro {
          margin: 0 0 1rem;
          color: var(--text-muted);
          line-height: 1.6;
        }
        .guide-list {
          display: grid;
          gap: 0.85rem;
        }
        .guide-item {
          display: flex;
          flex-direction: column;
          gap: 0.25rem;
          padding: 0.8rem 0.9rem;
          border: 1px solid var(--border);
          border-radius: 12px;
          background: var(--bg-elevated);
        }
        .guide-item strong {
          font-size: 0.95rem;
        }
        .guide-item span {
          color: var(--text-muted);
          line-height: 1.5;
          font-size: 0.9rem;
        }
      `}</style>
    </div>
  )
}
