import "./Tabs.css";

export default function Tabs({ current, onChange }) {
  return (
    <div className="tabs-container">
      <button
        className={current === "heatmap" ? "tab active" : "tab"}
        onClick={() => onChange("heatmap")}
      >
        Heatmap
      </button>

      <button
        className={current === "forecast" ? "tab active" : "tab"}
        onClick={() => onChange("forecast")}
      >
        Forecast
      </button>
    </div>
  );
}
