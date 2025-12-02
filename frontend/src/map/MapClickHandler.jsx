import { useMapEvent } from "react-leaflet";

function MapClickHandler({ onClick, onForecast }) {
  const API = import.meta.env.VITE_API_URL;

  useMapEvent("click", async (e) => {
    const lat = e.latlng.lat;
    const lng = e.latlng.lng;

    // Update marker position
    onClick({ lat, lng });

    // Fetch backend forecast
    try {
      const res = await fetch(`${API}/forecast?lat=${lat}&lng=${lng}`);
      
      if (!res.ok) {
        throw new Error(`Failed to fetch forecast (${res.status})`);
      }
      
      const data = await res.json();
      onForecast(data);
      
    } catch (err) {
      console.error("Forecast fetch error:", err);
      onForecast(null); // Signal error to component
    }
  });

  return null;
}

export default MapClickHandler;
