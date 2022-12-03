export const isDevelopment = window.location.hostname === "http://127.0.0.1" || window.location.hostname == "localhost"
// export const VIZ_BACKEND_URL = isDevelopment ? "http://127.0.0.1:5001/viz_analysis" : ""
export const VIZ_BACKEND_URL = isDevelopment ? "http://127.0.0.1:7777/viz_analysis" : "http://34.227.171.231:7777/viz_analysis"
