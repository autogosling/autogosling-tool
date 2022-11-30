export const isDevelopment = window.location.hostname === "http://127.0.0.1" || window.location.hostname == "localhost"
// export const VIZ_BACKEND_URL = isDevelopment ? "http://127.0.0.1:5001/viz_analysis" : ""
export const VIZ_BACKEND_URL = isDevelopment ? "http://127.0.0.1:5001/viz_analysis" : "https://autogosling-flask.loca.lt/viz_analysis"