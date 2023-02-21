export const isDevelopment = window.location.hostname === "http://127.0.0.1" || window.location.hostname == "localhost"
// export const VIZ_BACKEND_URL = isDevelopment ? "http://127.0.0.1:5001/viz_analysis" : ""
export const VIZ_BACKEND_URL = isDevelopment ? "http://127.0.0.1:7777/viz_analysis" : "http://34.227.171.231:7777/viz_analysis"
export const GROUND_VIZ_BACKEND_URL = isDevelopment ? "http://127.0.0.1:7777/true_viz_analysis" : "http://34.227.171.231:7777/true_viz_analysis"
export const RECONSTRUCT_URL = isDevelopment ? "http://127.0.0.1:7777/reconstruct" : "http://34.227.171.231:7777/reconstruct"

