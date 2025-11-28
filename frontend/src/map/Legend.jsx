import { useEffect } from "react";
import { useMap } from "react-leaflet";
import L from "leaflet";
import "./legend.css";

export default function Legend() {
  const map = useMap(); // <-- ALWAYS provides the actual map safely

  useEffect(() => {
    const legend = L.control({ position: "bottomright" });

    legend.onAdd = function () {
      const div = L.DomUtil.create("div", "pollen-legend");

      const colors = ["#D3D3D3", "#008000", "#32CD32", "#FFFF00", "#FFA500", "#FF4500"];
      const labels = ["No Data", "Very Low", "Low", "Moderate", "High", "Very High"];

      for (let i = 0; i < labels.length; i++) {
        div.innerHTML += `
          <div class="legend-item">
            <span class="legend-color" style="background:${colors[i]}"></span>
            <span class="legend-label">${labels[i]}</span>
          </div>`;
      }

      return div;
    };

    legend.addTo(map);   // <-- SAFE: map is guaranteed to exist

    return () => {
      legend.remove();
    };
  }, [map]);

  return null;
}
