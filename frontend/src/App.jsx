import { MapContainer, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";

function App() {
  return (
    <div style={{ width: "100vw", height: "100vh" }}>
      <MapContainer
        center={[-37.8136, 144.9631]} // Melbourne
        zoom={6}
        style={{ width: "100%", height: "100%" }}
      >
        <TileLayer url="https://tile.openstreetmap.org/{z}/{x}/{y}.png"/>

        {/* Pollen tiles served by FastAPI */}
        <TileLayer
          url="http://localhost:8000/pollen/GRASS_UPI/{z}/{x}/{y}"
          tileSize={256}
          maxZoom={16}
          minZoom={3}
          opacity={0.8}
        />
        
      </MapContainer>
    </div>
  );
}

export default App;
