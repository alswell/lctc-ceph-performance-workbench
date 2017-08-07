import { request, config } from '../utils'
import { fetch } from './restfulService'
const { api } = config
const { dashboard } = api

export async function myCity (params) {
  return request({
    url: 'http://www.zuimeitianqi.com/zuimei/myCity',
    data: params,
  })
}

export async function queryWeather (params) {
  return request({
    url: 'http://www.zuimeitianqi.com/zuimei/queryWeather',
    data: params,
  })
}

export async function query (params) {
  //let r = request({
  let r = fetch({
    url: 'dashboard',
    method: 'get',
    data: params,
  })
  console.log(r)
  return r
}
