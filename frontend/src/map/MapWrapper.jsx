import { useState } from "react";
import { MapContainer, TileLayer } from "react-leaflet";
import Legend from "./Legend";
import MapClickHandler from "./MapClickHandler";
import MapMarker from "./MapMarker";
import BottomDrawer from "./BottomDrawer";
import "leaflet/dist/leaflet.css";

function MapWrapper() {
  const [marker, setMarker] = useState(null);
  const [forecast, setForecast] = useState(null);


  return (
    <div style={{ width: "100%", height: "100%", position: "relative", overflow: "hidden",}}>
      <MapContainer
        center={[-37.8136, 144.9631]}
        zoom={6}
        style={{ width: "100%", height: "100%" }}
      >
        <Legend />

        {/* Listen for map clicks */}
        <MapClickHandler onClick={setMarker} onForecast={setForecast} />

        {/* Base map */}
        <TileLayer url="https://tile.openstreetmap.org/{z}/{x}/{y}.png" />

        {/* Pollen Heatmap */}
        <TileLayer
          url="http://localhost:8000/pollen/GRASS_UPI/{z}/{x}/{y}"
          tileSize={256}
          maxZoom={16}
          minZoom={3}
          opacity={0.8}
        />

        {/* Render dropped pin */}
        {marker && <MapMarker position={marker} />}
      </MapContainer>

      {/* Bottom Drawer */}
      <BottomDrawer marker={marker} forecast={forecast} />
    </div>
  );
}

export default MapWrapper;
