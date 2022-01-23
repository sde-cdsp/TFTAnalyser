import Document, { Html, Head, Main, NextScript } from 'next/document'

export default class MyDocument extends Document {
    render(): React.ReactElement {
        return (
            <Html lang="fr">
                <Head />
                <body>
                    <Main />
                    <NextScript />
                </body>
            </Html>
        )
    }
}
