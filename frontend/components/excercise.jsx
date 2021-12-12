import React, { Component } from 'react';

import { View, Image, StyleSheet, Text } from 'react-native';

class Excercise extends Component {

    constructor(props){
        super(props);
    }

    render() {
        return (
        <View>
            <Text
            style={{
                marginTop: 50,
                fontSize: 25,
                textAlign: 'center',
                fontWeight: 'bold',
                color: '#ffffff'
            }}>{this.props.data.excercise.name}</Text>
            <Text
             style={{
                marginTop: 10,
                textAlign: 'center',
                fontSize: 15,
                color: '#ffffff'
            }}>Core Joints Involved - {this.props.data.excercise.category}</Text>
            <Text
             style={{
                marginTop: 10,
                textAlign: 'center',
                color: '#ffffff',
                fontSize: 15,
            }}>Instructions</Text>
            <Text
             style={{
                marginTop: 10,
                textAlign: 'center',
                color: '#ffffff',
                fontSize: 15,
            }}>{this.props.data.excercise.description}</Text>
            <Image style={[
                {
                    marginTop: 10,
                },
                styles.image]} 
            source={{uri:this.props.data.excercise.url }} />
             
        </View>
        );
      }
    }



const styles = StyleSheet.create({
    image: {
        aspectRatio: 1,
    }
});


export default Excercise;