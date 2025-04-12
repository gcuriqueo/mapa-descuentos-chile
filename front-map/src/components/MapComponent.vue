.descuento {
color: red;
}<template>
  <div class="map-container">

    <!-- Barra de fecha -->
    <div class="fecha-bar">
      <div class="fecha-exportacion">
        {{ fechaExportacion ? formatearFecha(fechaExportacion) : '' }}
      </div>
    </div>

    <!-- Filtros -->
    <div class="filtros-container">
      <div class="filtro-grupo">
        <label>Banco:</label>
        <select v-model="bancoSeleccionado" class="filtro-select">
          <option value="">Todos los bancos</option>
          <option v-for="banco in bancosList" :key="banco" :value="banco">{{ banco }}</option>
        </select>
      </div>
      <div class="filtro-grupo">
        <label>Día:</label>
        <select v-model="diaSeleccionado" class="filtro-select">
          <option value="">Todos los días</option>
          <option v-for="dia in diasList" :key="dia" :value="dia">{{ dia }}</option>
        </select>
      </div>
      <div class="filtros-acciones">
        <button @click="limpiarFiltros" class="btn-limpiar">Limpiar filtros</button>
      </div>
      <div class="contador-resultados">
        {{ sitiosFiltrados.length }} resultados encontrados
      </div>
    </div>

    <!-- Control de radio -->
    <div v-if="miUbicacion" class="radio-control">
      <label>Radio: {{ (radio / 1000).toFixed(1) }} km</label>
      <input type="range" v-model="radioKm" min="0.5" max="10" step="0.5" class="slider" @input="actualizarRadio">
    </div>

    <!-- Mapa -->
    <div class="mapa-wrapper">
      <l-map :zoom="zoom" :center="center">
        <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
        <div v-for="(sitio, index) in sitiosFiltrados" :key="index">
          <l-marker v-for="(direccion, indexDireccion) in sitio.direcciones"
                    :key="`${index}-${indexDireccion}`"
                    :lat-lng="getLatLng(direccion)">
            <l-popup>
              <p class="popup-content">
                <strong>Banco:</strong> {{ sitio.banco }}<br>
                <strong>Nombre:</strong> {{ sitio.nombre }}<br>
                <strong>Descuento:</strong> <strong style="color: red;">{{ sitio.descuento }}</strong><br>
                <strong>Día:</strong> {{ sitio.dia }}<br>
                <strong>Dirección:</strong> {{ direccion.direccion }}
              </p>
            </l-popup>
          </l-marker>
        </div>
        <l-marker v-if="miUbicacion" :lat-lng="miUbicacion" :icon="iconoMiUbicacion"></l-marker>
        <l-circle v-if="miUbicacion" :lat-lng="miUbicacion" :radius="radio" color="green" :key="miUbicacion"></l-circle>
      </l-map>
    </div>
  </div>
</template>

<script>
import { LMap, LTileLayer, LMarker, LPopup, LCircle } from 'vue2-leaflet';
import { Icon, icon } from 'leaflet';
import 'leaflet/dist/leaflet.css';
import axios from 'axios';

delete Icon.Default.prototype._getIconUrl;

Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

export default {
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup,
    LCircle
  },
  data() {
    return {
      sitios: [],
      zoom: 13,
      center: [-33.412860, -70.597314],
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution: '© OpenStreetMap contributors',
      miUbicacion: null,
      iconoMiUbicacion: icon({
        iconUrl: 'https://raw.githubusercontent.com/gcuriqueo/map/master/icons/marker-icon-red.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41]
      }),
      radio: (5 * 1000), // metros
      bancoSeleccionado: '',
      diaSeleccionado: '',
      radioKm: 5,
      fechaExportacion: null,
    };
  },
  computed: {
    // Obtener lista única de bancos para el selector
    bancosList() {
      const bancos = [...new Set(this.sitios.map(sitio => sitio.banco))];
      return bancos.sort();
    },

    // Obtener lista simplificada de días para el selector
    diasList() {
      return ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'];
    },

    // Sitios filtrados según las selecciones
    sitiosFiltrados() {
      return this.sitios.filter(sitio => {
        // Verificar que tenga coordenadas válidas
        const tieneCoordenadasValidas = sitio.direcciones &&
            sitio.direcciones.length > 0 &&
            sitio.direcciones[0] &&
            sitio.direcciones[0].coordenadas;

        // Aplicar filtro de banco
        const coincideBanco = !this.bancoSeleccionado || sitio.banco === this.bancoSeleccionado;

        // Aplicar filtro de día (busca si el día seleccionado está contenido en el texto del día)
        const coincideDia = !this.diaSeleccionado ||
            (sitio.dia && sitio.dia.includes(this.diaSeleccionado));

        return tieneCoordenadasValidas && coincideBanco && coincideDia;
      });
    }
  },
  methods: {
    getLatLng(direccion) {
      if (direccion && direccion.coordenadas) {
        return [direccion.coordenadas.latitud, direccion.coordenadas.longitud];
      }
      return null;
    },

    // Método para limpiar los filtros
    limpiarFiltros() {
      this.bancoSeleccionado = '';
      this.diaSeleccionado = '';
    },

    // Método para actualizar el radio desde el slider
    actualizarRadio() {
      this.radio = this.radioKm * 1000;
    },
    formatearFecha(fechaStr) {
      const meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
      const fecha = new Date(fechaStr);
      return `${meses[fecha.getMonth()]} ${fecha.getFullYear()}`;
    }
  },
  async created() {
    // Obtener ubicación del usuario
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(position => {
        this.miUbicacion = [position.coords.latitude, position.coords.longitude];
        this.center = this.miUbicacion;
      });
    }

    // Cargar datos
    try {
      const response = await axios.get('http://localhost:8100/data/food/banks/coordinates.json');
      this.sitios = response.data.datos;
      this.fechaExportacion = response.data.fecha_extraccion;
    } catch (error) {
      console.error('Error al cargar los datos:', error);
    }
  }
};
</script>

<style>
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

.map-container {
  height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
}

.filtros-container {
  background-color: #4d83da;
  color: white;
  padding: 16px;
  border-bottom: 1px solid #3973ca;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 16px;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

.filtro-grupo {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filtro-select {
  padding: 8px 12px;
  border: 1px solid #3973ca;
  border-radius: 4px;
  font-size: 14px;
  min-width: 180px;
  background-color: white;
}

.filtros-acciones {
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn-limpiar {
  padding: 8px 12px;
  background-color: #2a62bc;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.btn-limpiar:hover {
  background-color: #1e4c99;
}

.contador-resultados {
  font-size: 14px;
  color: white;
  font-weight: bold;
}

.mapa-wrapper {
  flex: 1;
  position: relative;
}

.popup-content {
  min-width: 200px;
  padding: 8px;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

.leaflet-popup-content {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

.radio-control {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  background-color: rgba(255, 255, 255, 0.8);
  padding: 10px 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  width: 300px;
}

.slider {
  width: 100%;
  height: 8px;
  background: #ddd;
  outline: none;
  border-radius: 4px;
  -webkit-appearance: none;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #4d83da;
  cursor: pointer;
}

.slider::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #4d83da;
  cursor: pointer;
}

.fecha-bar {
  background-color: #3973ca;
  color: white;
  padding: 8px 16px;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  border-bottom: 1px solid #2a62bc;
}

.fecha-exportacion {
  font-weight: bold;
  font-size: 16px;
}

</style>