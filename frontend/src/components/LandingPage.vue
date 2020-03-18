<template>
  <div class="container">
    <div class="row">
      <div class="col-md-6 offset-md-3 text-center">
        <div class="card card-block p-3">
          <h4 class="title">COVID-19 Outbreak Upates</h4>
          <h5 class="subtitle">
            Click
            <a href="/info">here</a> for more info
          </h5>
          <h6 class="error">
            {{ error  }}
          </h6>
          <div class="col-md-8 col-sm-10 offset-md-2 offset-sm-1 mt-3">
            <form @submit="onSubmit">
              <div class="form-row mb-3">
                <div class="col">
                  <VueTelInput v-on:change-tel="changeTel" />
                </div>
              </div>
              <div class="form-row">
                <div class="col">
                  <VueGoogleAutoComplete v-on:change-place="changePlace" />
                </div>
              </div>
              <button type="submit" value class="btn btn-dark col-10 mt-4 mb-3">Sign up</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import VueGoogleAutoComplete from '@/components/VueGoogleAutocomplete'
import VueTelInput from '@/components/VueTelInput'
import { mapActions, mapGetters } from 'vuex'

export default {
  components: {
    VueGoogleAutoComplete,
    VueTelInput
  },
  data () {
    return {
      telephone: '',
      location: {}
    }
  },
  methods: {
    ...mapActions(['addSubscriber']),
    changeTel (telephone) {
      this.telephone = telephone
    },
    changePlace (location) {
      this.location = location
    },
    onSubmit (e) {
      e.preventDefault()
      let location = JSON.stringify(this.location)
      let telephone = this.telephone
      const data = {
        telephone,
        location
      }
      this.addSubscriber(data)
    }
  },
  computed: mapGetters(['error'])
}
</script>

<style scoped>
.card {
  background-color: rgb(245, 245, 245, 0.9);
  border: 1px solid lime;
  margin-top: 25%;
}

.btn-dark {
  border: 1px solid lime;
}
.error {
  color: red;
}
.title {
  font-weight: 800;
}
.subtitle {
  font-weight: 400;
}
</style>
