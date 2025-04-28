import dotenv from "dotenv";
dotenv.config();

export default class Env {
  static get URL() {
    return process.env.URL || "";
  }

  static get ADMIN_NAME() {
    return process.env.ADMIN_NAME || "";
  }

  static get ADMIN_PASSWORD() {
    return process.env.ADMIN_PASSWORD || "";
  }
  static get USER_NAME(){
    return process.env.USER_NAME || "";
  }
static get USER_PASS(){
    return process.env.USER_PASS || "";
  }}
  