import api from "./axiosConfig";

export const getRutas = () => api.get("/rutas");
export const createRuta = (payload) => api.post("/rutas", payload);
export const updateRuta = (id, payload) => api.put(`/rutas/${id}`, payload);
export const deleteRuta = (id) => api.delete(`/rutas/${id}`);
