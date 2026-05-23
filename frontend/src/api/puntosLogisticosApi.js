import api from "./axiosConfig";

export const getPuntosLogisticos = () => api.get("/puntos-logisticos");
export const createPuntoLogistico = (payload) => api.post("/puntos-logisticos", payload);
export const updatePuntoLogistico = (id, payload) => api.put(`/puntos-logisticos/${id}`, payload);
export const deletePuntoLogistico = (id) => api.delete(`/puntos-logisticos/${id}`);
