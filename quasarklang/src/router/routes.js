
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    meta: {
      title: 'Child component'
    },
    children: [
      { path: '', component: () => import('pages/Index.vue') },
      { path: '/conlls/:filename', component: () => import('src/pages/Klang.vue'), 
        props: true},

    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '*',
    component: () => import('pages/Error404.vue')
  }
]

export default routes
