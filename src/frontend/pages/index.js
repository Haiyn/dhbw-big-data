import Head from 'next/head'
import { connectToDatabase } from '../util/mongodb'
import { Box, Card, Image, Heading, Text, Flex, Button } from 'rebass'
import { Label, Input } from '@rebass/forms'
import React, { useState, useEffect } from 'react';
import useSWR from 'swr'

const fetcher = url => fetch(url).then(res => res.json());

export default function Home({ isConnected }) {
  const [ multiverseid, setMultiverseid ] = useState("");
  const [ name, setName ] = useState("");
  const [ artist, setArtist ] = useState("");
  const [ cards, setCards ] = useState([]);




  const get_cards = (e) => {
    console.log("Getting cards with parameters.");
    console.log("Artist " + artist);
    console.log("ID " + multiverseid);
    console.log("Name " + name);
    let api_route = '/api/cards';
    api_route += multiverseid !== "" ? multiverseid : "";
    api_route += name !== "" ? name : "";
    api_route += artist !== "" ? artist : "";
    console.log(api_route)
    //setCards(useSWR(api_route, fetch));
  }



  return (
    <Flex className="container">
      <Head>
        <title>MTG Card Search</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main>
        <Heading fontSize={[ 5 ]}>
          Magic The Gathering Card Search
        </Heading>

        {isConnected ? (
          <Heading fontSize={[ 4 ]}>You are connected and ready to search!</Heading>
        ) : (
          <h2 className="subtitle">
            You are NOT connected to MongoDB. Check the <code>README.md</code>{' '}
            for instructions.
          </h2>
        )}
        <Flex mx={-2} mb={3}>
          <Box width={1/2} px={2}>
            <Label htmlFor='input_multiverse_id'>Multiverse ID</Label>
            <Input
              id='input_multiverse_id'
              name='input_multiverse_id'
              type='number'
              placeholder='1234'
              onChange={(e) => setMultiverseid(e.target.value)}
            />
          </Box>

          <Box width={1/2} px={2}>
            <Label htmlFor='input_card_name'>Filter card names</Label>
            <Input
              id='input_card_name'
              name='input_card_name'
              type='text'
              placeholder='Card name contains...'
              onChange={(e) => setName(e.target.value)}
            />
          </Box>

          <Box width={1/2} px={2}>
            <Label htmlFor='input_artist_name'>Filter artist names</Label>
            <Input
              id='input_artist_name'
              name='input_artist_name'
              type='text'
              placeholder='Artist name contains...'
              onChange={(e) => setArtist(e.target.value)}
            />
          </Box>
        </Flex>

        <Button onClick={fetcher('api/cards').then(res => setCards(res))} variant='primary' style={{ background: "blue"}}>Search Now</Button>


        <Flex mx={-2} mb={3}>
          {cards.map((card) => (
            <Box width={256}>
              <Card
                sx={{
                  p: 1,
                  borderRadius: 2,
                  boxShadow: '0 0 16px rgba(0, 0, 0, .25)',
                }}>
                <Image src={ "http://gatherer.wizards.com/Handlers/Image.ashx?type=card&multiverseid=" + card.multiverseid} />
                <Box px={2}>
                  <Heading>
                    {card.name}
                  </Heading>
                  <Text className="description" fontSize={2}>
                    {card.artist}
                  </Text>
                  <Text className="description" fontSize={0}>
                    {card.text}
                  </Text>
                </Box>
              </Card>
            </Box>
          ))}
        </Flex>
      </main>
    </Flex>
  )
}

export async function getServerSideProps(context) {
  const { client } = await connectToDatabase()

  const isConnected = await client.isConnected()

  return {
    props: { isConnected },
  }
}
