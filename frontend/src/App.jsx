import { MapContainer, TileLayer, useMap } from "react-leaflet";
import { useState } from "react";
import "leaflet/dist/leaflet.css";
import Legend from "./Legend";

function MapWithLegend() {
  const map = useMap();
  window.mapInstance = map; // expose map instance globally for legend
  return null;
}


function App() {

  const [mode, setMode] = useState("heatmap");


  return (
    <div style={{ width: "100vw", height: "100vh" }}>

      <MapContainer
        center={[-37.8136, 144.9631]} // Melbourne
        zoom={6}
        style={{ width: "100%", height: "100%" }}
      >
        <MapWithLegend />
        <Legend />

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
