import React from "react";
import { Image } from "react-native";
import { Layout } from "@ui-kitten/components";

export class Other extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    return (
      <Layout
        style={{ justifyContent: "center", alignItems: "center", flex: 1 }}
      >
        <Image
          style={{ height: 200, width: 200, borderRadius: 50 }}
          source={{
            uri: "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Ipomoea_batatas_006.JPG/1920px-Ipomoea_batatas_006.JPG",
          }}
        />
      </Layout>
    );
  }
}
