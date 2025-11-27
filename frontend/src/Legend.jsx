import { useEffect } from "react";
import L from "leaflet";
import "./legend.css";


export default function Legend() {
  useEffect(() => {
    const legend = L.control({ position: "bottomright" });

    legend.onAdd = function () {
      const div = L.DomUtil.create("div", "pollen-legend");

      const grades = [0, 1, 2, 3, 4, 5];
      const colors = ["#D3D3D3", "#008000", "#32CD32", "#FFFF00", "#FFA500", "#FF4500"];
      const labels = ["No Data", "Very Low", "Low", "Moderate", "High", "Very High"];

      for (let i = 0; i < grades.length; i++) {
        div.innerHTML +=
          `<div class="legend-item">
             <span class="legend-color" style="background:${colors[i]}"></span>
             <span class="legend-label">${labels[i]}</span>
           </div>`;
      }

      return div;
    };

    legend.addTo(window.mapInstance); // We will set this in App.jsx

    return () => {
      legend.remove();
    };
  }, []);

  return null;
}
