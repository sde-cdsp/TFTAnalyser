import type { AppProps } from 'next/app'

import { DefaultSeo } from 'next-seo'

import 'styles/index.css'

const MyApp = ({ Component, pageProps }: AppProps): React.ReactElement => (
    <>
        <DefaultSeo title="My site" />
        <Component {...pageProps} />
    </>
)

export default MyApp
