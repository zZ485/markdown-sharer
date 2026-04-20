import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

export default {
  getDocuments() {
    return api.get('/documents')
  },
  getDocument(id) {
    return api.get(`/documents/${id}`)
  },
  createDocument(data) {
    return api.post('/documents', data)
  },
  updateDocument(id, data) {
    return api.put(`/documents/${id}`, data)
  },
  deleteDocument(id) {
    return api.delete(`/documents/${id}`)
  },
  createShare(id) {
    return api.post(`/documents/${id}/share`)
  },
  getSharedDocument(token) {
    return api.get(`/share/${token}`)
  },
}
