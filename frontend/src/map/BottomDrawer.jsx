import { useState, useEffect } from "react";

export default function BottomDrawer({ marker }) {
  const [isOpen, setIsOpen] = useState(false);

  // When marker changes, auto-open drawer
  useEffect(() => {
    if (marker) setIsOpen(true);
  }, [marker]);

  if (!marker || !isOpen) return null;

  return (
    <div
      style={{
        position: "absolute",
        bottom: 0,
        left: 0,
        width: "100%",
        height: "25vh",
        background: "#000000e1",
        padding: "20px",
        borderTop: "1px solid #ccc",
        backdropFilter: "blur(6px)",
        boxShadow: "0 -2px 10px rgba(0,0,0,0.2)",
        zIndex: 1000,
      }}
    >
      <button
        onClick={() => setIsOpen(false)}
        style={{
          position: "absolute",
          top: 10,
          right: 45,
          background: "transparent",
          border: "none",
          fontSize: "20px",
          cursor: "pointer",
        }}
      >
        ✖
      </button>

      <strong>📍 Selected Location</strong>
      <div>Latitude: {marker.lat.toFixed(6)}</div>
      <div>Longitude: {marker.lng.toFixed(6)}</div>
    </div>
  );
}
