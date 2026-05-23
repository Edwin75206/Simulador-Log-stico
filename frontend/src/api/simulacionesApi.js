import api from "./axiosConfig";

export const getSimulaciones = () => api.get("/simulaciones");
export const getSimulacion = (id) => api.get(`/simulaciones/${id}`);
export const createSimulacion = (payload) => api.post("/simulaciones", payload);
export const getResultados = (id) => api.get(`/simulaciones/${id}/resultados`);
export const deleteSimulacion = (id) => api.delete(`/simulaciones/${id}`);
