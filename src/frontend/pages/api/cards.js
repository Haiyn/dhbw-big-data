import { connectToDatabase } from "../../util/mongodb";

export default async (req, res) => {
  const { db } = await connectToDatabase();

  const cards = await db
    .collection("Cards")
    .find( {
      //"multiverseid": req.query.multiverseid,
      //"artist": req.query.artist,
      //"name": req.query.name,
    } )
    .toArray();

  res.json(cards);

};