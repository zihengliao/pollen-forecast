import { Marker, Popup } from "react-leaflet";
import L from "leaflet";

// Fix Leaflet icons once here
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});

function MapMarker({ position }) {
  return (
    <Marker position={[position.lat, position.lng]}>
      <Popup>
        <b>Latitude:</b> {position.lat.toFixed(5)} <br />
        <b>Longitude:</b> {position.lng.toFixed(5)}
      </Popup>
    </Marker>
  );
}

export default MapMarker;
