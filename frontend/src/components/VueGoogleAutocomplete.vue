<template>
    <div>

        <vue-google-autocomplete ref="address" id="map" name="location" autocomplete="off" classname="form-control" types="(cities)" placeholder="Please type your city" v-on:placechanged="getAddressData">
        </vue-google-autocomplete>
    </div>
</template>

<script>
import VueGoogleAutocomplete from 'vue-google-autocomplete'

export default {
  components: { VueGoogleAutocomplete },

  data: function () {
    return {
      address: ''
    }
  },

  mounted () {
    // To demonstrate functionality of exposed component functions
    // Here we make focus on the user input
    this.$refs.address.focus()
  },

  methods: {
    /**
         * When the location found
         * @param {Object} addressData Data of the found location
         * @param {String} id Input container ID
         */
    getAddressData: function (addressData, id) {
      this.$emit('change-place', addressData)
    }
  }
}
</script>
