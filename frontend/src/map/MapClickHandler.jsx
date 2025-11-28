import { useMapEvent } from "react-leaflet";

function MapClickHandler({ onClick, onForecast }) {
  useMapEvent("click", (e) => {
    const lat = e.latlng.lat;
    const lng = e.latlng.lng;

    // Update marker position
    onClick({ lat, lng });

    // Fetch backend forecast
    fetch(`http://localhost:8000/forecast?lat=${lat}&lng=${lng}`)
      .then((res) => res.json())
      .then((data) => {
        onForecast(data);   // Store forecast in state
      })
      .catch((err) => console.error("Forecast fetch error:", err));
  });

  return null;
}

export default MapClickHandler;
