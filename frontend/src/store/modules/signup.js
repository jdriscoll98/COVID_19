import axios from 'axios'
import router from '../../router'

const state = {
  succes: false,
  verify_user: ''
}

const getters = {}

const mutations = {
  verifySubscriber: (state, { telephone }) => {
    state.verify_user = telephone
    router.push('/verify')
  },
  checkCode: (state, status) => {
    console.log(status)
    if (status === 200) {
      router.push('/thankyou')
    } else {
      console.log('not valid status')
    }
  }
}

const actions = {
  async beginFlow ({ commit }, { telephone }) {
    console.log('begin flow')
    const response = await axios.post('api/subscribers/begin_flow', {
      telephone
    })
    if (response.status === 200) {
      console.log('good response')
    } else {
      console.log('Bad response')
    }
  },
  async addSubscriber ({ commit }, { telephone, location }) {
    const response = await axios.post('api/subscribers', {
      telephone,
      location
    })

    commit('verifySubscriber', response.data)
  },
  async verifyCode ({ commit }, key) {
    const telephone = state.verify_user

    const response = await axios.post('api/subscribers/verify', {
      key,
      telephone
    })
    commit('checkCode', response.status)
    if (response.status === 200) {
      console.log('response good')
      this.dispatch('beginFlow', {
        telephone
      })
    } else {
      console.log('response bad')
    }
  }
}

export default {
  state,
  getters,
  mutations,
  actions
}
