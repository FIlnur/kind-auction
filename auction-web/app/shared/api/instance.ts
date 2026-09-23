// app/shared/api/instance.ts
import axios from 'axios';

export const api = axios.create({
  baseURL: 'https://api.github.com',
  timeout: 10000,
});