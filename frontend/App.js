import { StyleSheet, Image, Text, View, FlatList, TouchableOpacity, SafeAreaView, ScrollView, LogBox} from 'react-native';
import { SearchBar } from 'react-native-elements';
import React, { useState, useEffect } from 'react';

import Excercise from './components/excercise';

export default function App() {
  const [data, setData] = useState([]);
  const [query, setQuery] = useState('');
  const [heroes, setHeroes] = useState([]);
  const [selected, setSelected] = useState(false);
  const [excercise, setExcercise] = useState({});
  const [searchResults, setSearchResults] = useState([]);
 
  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    LogBox.ignoreLogs(['VirtualizedLists should never be nested']);
  }, [])

  // Please replace URL
  const fetchData = async () => {
    fetch(
      "www.backendurl.com/dataset")
    .then((response) => response.json())
    .then((json) => {
      setData(json);
      setHeroes(json.slice());
    })
    .catch( error => {
      console.error(error);
    });
  };
  

  const filterNames = (hero) => {
    // console.log(query);
    return formatNames(hero);
  }

  const formatNames = (hero) =>{
    let heroName = hero.name;
    return heroName;
  }

  const updateQuery = (input) => {
    setSelected(false);
    setHeroes(data.slice());
    setQuery(input);
    setSearchResults(heroes.filter((hero) => hero.name.toLowerCase().startsWith(input.toLowerCase())));
  }

  const onPress = (input) => {
    console.log(input);
    setSelected(true);
    setExcercise(input);
    setQuery(input.name)
  }


  return (
      <SafeAreaView style={styles.container}>
      <ScrollView style={styles.scrollView}>
      <Text style={[styles.white, styles.heading]}>
      <Image
          style={{
            width:40,
            height: 40,
            tintColor: '#ffffff'
          }}
          source={require('./assets/front.png')}
        />
        <Text> {'   '}Blazepose Exercise Search{'   '}</Text>
        <Image
          style={{
            width:40,
            height: 40,
            tintColor: '#ffffff'
          }}
          source={require('./assets/flipped_icon.png')}
        />
        </Text>
      <SearchBar
          style={{
            color: '#ffffff',
          }}
          onChangeText={updateQuery}
          value={query}   
          placeholder="Search for Exercise...."
      />
      {
        !selected ? 
        <View>
      <FlatList  data={searchResults} keyExtractor = {(i)=>i.name.toString()}
        extraData = {query} 
        renderItem = {({item}) => (
          <TouchableOpacity onPress={() => onPress(item)}>
              <Text
                style={styles.flatList}>{filterNames(item)}
                </Text>
            </TouchableOpacity>
        )
          } />
          </View> : <Excercise data={{excercise}}/>
      }    
      </ScrollView>  
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
      backgroundColor: '#21253a',
      flex: 1,
  },
  heading:{
      fontSize: 25
  },
  flatList:{
      paddingLeft: 15, 
      marginTop:15, 
      paddingBottom:15,
      fontSize: 20,
      borderBottomColor: '#26a69a',
      borderBottomWidth:1,
      color: "#ffffff"
  },
  item: {
    padding: 20,
    marginVertical: 8,
    marginHorizontal: 16,
  },
  image: {
    height: 250,
    width: 250
    },
  white: {
    color: '#ffffff'
  }
});
