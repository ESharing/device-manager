/**
 * @jest-environment jsdom
 */

import Vue from 'vue'
import { shallowMount } from '@vue/test-utils';

import mockAxiosTest from '@/components/HelloWorld.vue'

import mockAxios from '@/__tests__/__mocks__/axios'
import { schemas as fakedata } from '@/__tests__/__mocks__/mockSchema'

describe('HelloWorld.vue', () => {
 it('获取Schema', () => {
   const wrapper = shallowMount(mockAxiosTest)
   mockAxios.get.mockImplementationOnce(() => {
     return Promise.resolve({
       data: {
         data: fakedata,
         error_code: 0,
         message: '',
       },
     })
   })
   wrapper.vm.fetchData()
   Vue.nextTick(() => {
     Vue.nextTick(() => {
       console.log("=====" + fakedata );
       expect(wrapper.vm.schemas).toEqual(fakedata)
     })
   })
 })
})