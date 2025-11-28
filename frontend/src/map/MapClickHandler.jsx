import { useMapEvent } from "react-leaflet";

function MapClickHandler({ onClick }) {
  useMapEvent("click", (e) => {
    onClick({
      lat: e.latlng.lat,
      lng: e.latlng.lng,
    });
  });

  return null;
}

export default MapClickHandler;
