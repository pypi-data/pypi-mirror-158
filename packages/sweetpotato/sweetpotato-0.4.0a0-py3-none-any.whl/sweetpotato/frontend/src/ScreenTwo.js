import React from "react";
import { Layout, Text } from "@ui-kitten/components";

export class ScreenTwo extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    return (
      <Layout
        style={{
          height: "100%",
          justifyContent: "center",
          alignItems: "center",
          flex: 1,
        }}
      >
        <Text>World</Text>
      </Layout>
    );
  }
}
