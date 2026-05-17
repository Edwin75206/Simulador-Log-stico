import api from "./axiosConfig";

export const getTransportes = () => api.get("/transportes");
export const createTransporte = (payload) => api.post("/transportes", payload);
export const updateTransporte = (id, payload) => api.put(`/transportes/${id}`, payload);
export const deleteTransporte = (id) => api.delete(`/transportes/${id}`);
