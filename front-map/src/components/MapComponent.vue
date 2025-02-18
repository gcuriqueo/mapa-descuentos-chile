<template>
    <div style="height: 100vh; width: 100%;">
      <l-map :zoom="zoom" :center="center">
        <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
        <div v-for="(sitio, index) in sitiosConCoordenadas" :key="index">
          <l-marker v-for="(direccion, indexDireccion) in sitio.direcciones" 
                    :key="`${index}-${indexDireccion}`" 
                    :lat-lng="getLatLng(direccion)">
            <l-popup>
              <p>
                <strong>Banco:</strong> {{ sitio.banco}}<br>
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
  </template>
  
  <script>
  import { LMap, LTileLayer, LMarker, LPopup, LCircle } from 'vue2-leaflet';
  import { Icon } from 'leaflet';
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
        url: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
        attribution: '© OpenStreetMap contributors',
        miUbicacion: null,
        iconoMiUbicacion: L.icon({
            iconUrl: 'https://raw.githubusercontent.com/gcuriqueo/map/master/icons/marker-icon-red.png',
            iconSize: [25, 41],
            iconAnchor: [12, 41]
        }),
        radio: (5 * 1000), // metros
      };
    },
    computed: {
        sitiosConDireccionYCoordenadas() {
          //console.log('Número de sitios:', this.sitios.length);
          this.sitios.forEach((sitio, index) => {
              console.log(`sitio ${index}:`, sitio);
          });
          const sitiosFiltrados = this.sitios.filter(sitio => sitio.direcciones.length > 0 && sitio.direcciones[0].coordenadas);
          //console.log('Número de sitios filtrados:', sitiosFiltrados.length);
          sitiosFiltrados.forEach(sitio => {
              if (sitio.direcciones[0].coordenadas === null || sitio.direcciones[0].coordenadas === undefined) {
                console.log('sitio.direcciones[0].coordenadas es null o undefined');
              } else {
                console.log(sitio.direcciones[0].coordenadas);
              }
          });
          return sitiosFiltrados;
        },
        sitiosConCoordenadas() {
            return this.sitios.filter(sitio => sitio.direcciones[0] && sitio.direcciones[0].coordenadas);
        }
  },

    methods: {
        getLatLng(direccion) {
            if (direccion && direccion.coordenadas) {
                //console.log("aqui las coordenadas:" ,direccion.coordenadas);
                return [direccion.coordenadas.latitud, direccion.coordenadas.longitud];
            }
            return null;
        }
    },

    async created() {
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(position => {
              this.miUbicacion = [position.coords.latitude, position.coords.longitude];
              this.center = this.miUbicacion;
          });
        }
        try {
          const response = await axios.get('http://localhost:8100/data/food/banks/coordinates.json');
          this.sitios = response.data;
        } catch (error) {
            console.error(error);
        }
    }
  };
  </script>

<style scoped>
.l-map {
  height: 100%;
  width: 100%;
}
</style>