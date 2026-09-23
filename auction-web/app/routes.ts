import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  // Главная страница (отвечает за путь /)
  index("./routes/home.tsx"),
  
  // Страница профиля (отвечает за путь /profile)
  route("profile", "./routes/profile.tsx"),
] satisfies RouteConfig;