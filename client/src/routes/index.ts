const router = createBrowserRouter([
    {
        path: "/"
        element: Home(),
    },
    {
        path: '/test',
        element:Test(),
    }
]),

export {router};