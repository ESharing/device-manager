/**
 * @jest-environment jsdom
 */

import { shallowMount } from '@vue/test-utils'
import App from '@/App.vue'
//import HelloWorld from '@/components/HelloWorld.vue'
/*
describe('App', () => {
  // Inspect the raw component options
  it('has data', () => {
    expect(typeof App.data).toBe('function')
  })
})
*/
describe('Mounted App', () => {
  const wrapper = shallowMount(App);

  test('does a wrapper exist', () => {
    expect(wrapper.exists()).toBe(true)
  })
})
/*
describe('HelloWorld', () => {
  test('is a Vue instance', () => {
    const wrapper = mount(HelloWorld)
    expect(wrapper.isVueInstance()).toBeTruthy()
  })
})
*/