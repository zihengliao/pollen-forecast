import { useState, useEffect } from "react";
import { POLLEN_LEVELS } from "../constants/pollenEnum";
import "./BottomDrawer.css";

export default function BottomDrawer({ marker, forecast }) {
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    if (marker) setIsOpen(true);
  }, [marker]);

  if (!marker || !forecast || !isOpen) return null;

  return (
    <div className="drawer">
      <button className="drawer-close" onClick={() => setIsOpen(false)}>
        ✖
      </button>

      <strong className="drawer-title">5-Day Grass Pollen Forecast</strong>

      <div className="forecast-container">
        {Object.entries(forecast).map(([date, value]) => (
          <div className="forecast-card" key={date}>
            <div className="forecast-date">{date}</div>
            <div className="forecast-value" style={{ color: POLLEN_LEVELS[value].color }}>
            {value}
            </div>

            <div className="forecast-label" style={{ color: POLLEN_LEVELS[value].color }}>
            {POLLEN_LEVELS[value].label}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
