#!/usr/bin/env python3
"""Writes the planning / comparison guides (kind: guide) into src/pages and registers them in site.json.
Re-runnable: overwrites the guide files it owns. Facts checked Oct 2026 (NPS fees page, NPS Skywalk page,
Grand Canyon Railway schedule, NPS North Rim fall-operations notice)."""
import json, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
site = json.load(open(ROOT / 'src/site.json'))
DATE = '2026-10-20'

CTA_DAY = '<p><a class="btn" href="/grand-canyon-day-tour-from-flagstaff/">See the Grand Canyon day tour from Flagstaff</a></p>'
CTA_PRIV = '<p><a class="btn" href="/private-tour-inquire-about-customized-private-tours/">Ask about a private tour</a></p>'
PICKUP = ('<div class="note"><strong>Pickup:</strong> hotel and vacation-rental pickup is included within Flagstaff city limits '
          '(and the Williams area on our Williams tour). We can often arrange other pickup points for an extra fee. '
          '<a href="/contact-us/">Ask us</a> before you book.</div>')

def tldr(items):
    return '<div class="tldr"><strong>The short version</strong><ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul></div>'

def table(head, rows):
    h = ''.join(f'<th>{c}</th>' for c in head)
    b = ''.join('<tr>' + ''.join((f'<th>{c}</th>' if i == 0 else f'<td>{c}</td>') for i, c in enumerate(r)) + '</tr>' for r in rows)
    return f'<div class="tblwrap"><table class="cmp"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'

def related(links):
    return '<div class="related"><h2>Related guides</h2><ul>' + ''.join(f'<li><a href="{u}">{t}</a></li>' for u, t in links) + '</ul></div>'

G = []
def guide(slug, h1, title, desc, cat, og, ogalt, rank, body):
    G.append(dict(slug=slug, h1=h1, title=title, desc=desc, cat=cat, og=og, ogalt=ogalt, rank=rank, body=body))

# ------------------------------------------------------------------ GETTING HERE
guide('phoenix-to-grand-canyon', 'Phoenix to the Grand Canyon: Drive Times, Routes and Why We’d Base in Flagstaff',
      'Phoenix to Grand Canyon: Drive Time, Routes & Tips | TrekWest',
      'How far is the Grand Canyon from Phoenix? About 230 miles and 3.5 to 4 hours each way. Routes, where to stop, and why a night in Flagstaff turns a long day into a great one.',
      'Getting here', 'img-3344', 'TrekWest van on a pine-lined road with the San Francisco Peaks behind', 1, f"""
{tldr(['Phoenix (Sky Harbor) to Grand Canyon Village is about 230 miles / 370 km: 3.5 hours with no stops, closer to 4 with traffic and a fuel stop.',
       'As a day trip that is 7 to 8 hours of driving for 3 to 4 hours at the rim. It can be done. We would not recommend it.',
       'Drive to Flagstaff the night before (2 to 2.5 hours), sleep at 7,000 ft, and the canyon is 80 miles away in the morning.',
       'We pick up in Flagstaff for our small-group day tours, so you can leave the rental car at the hotel.'])}
<h2>How far is the Grand Canyon from Phoenix?</h2>
<p>From central Phoenix or Sky Harbor airport to the South Rim entrance it is roughly 230 miles. Google will tell you 3 hours 30 minutes. Real life, with a coffee stop and the slow stretch through the Verde Valley climb, is usually 3 hours 45 minutes to 4 hours. Scottsdale adds 15 to 20 minutes; Mesa, Chandler and Gilbert add a little more.</p>
<p>The route is simple: <strong>I-17 north</strong> for about 145 miles to Flagstaff, then either <strong>US-180 north-west</strong> through the ponderosa forest straight to the South Entrance (the prettier way, 80 miles), or I-40 west to Williams and <strong>SR-64 north</strong> (the faster way in winter when US-180 is icy). Both land you at the same place.</p>
<h2>Can you do Phoenix to the Grand Canyon in a day?</h2>
<p>Yes, and thousands of people do. Here is what that day looks like: leave at 6 am, arrive around 10, see Mather Point and the Village, grab lunch, drive back by 3 pm to beat the dark and the Phoenix evening traffic, home at 7. You will have spent about 8 hours in a car for 4 hours at one of the great places on Earth, most of it in the flat midday light that makes the canyon look like a postcard left in the sun.</p>
<p>Our honest advice, as people who drive to the rim every day: <strong>split it.</strong></p>
<h2>The better plan: a night (or two) in Flagstaff</h2>
<p>Flagstaff is 2 to 2.5 hours from Phoenix on I-17, and it is a genuinely nice place to be: a historic downtown on Route 66, a university town with good restaurants and breweries, and 7,000 feet of elevation that makes summer evenings 20 degrees cooler than the Valley. From Flagstaff the South Rim is 80 miles, about 1.5 hours.</p>
<ol>
<li><strong>Day 1:</strong> drive up in the afternoon, stop at Montezuma Castle or <a href="/camp-verde-day-trip-from-flagstaff/">Camp Verde</a> on the way, dinner downtown (<a href="/best-places-to-eat-in-flagstaff-arizona/">our picks</a>).</li>
<li><strong>Day 2:</strong> the canyon. Either drive yourself, or let us collect you from your hotel at 8 am, handle the park entrance, the parking, the lunch and the route, and drop you back around 5:30 pm having seen the Village, the East Rim overlooks and the Desert View Watchtower with a guide who can explain what you are looking at.</li>
<li><strong>Day 3 (optional):</strong> an easy morning hike near town, <a href="/best-places-to-see-fall-leaves-in-flagstaff/">aspens in autumn</a>, or Walnut Canyon and Sunset Crater on the way back south.</li>
</ol>
{PICKUP}
<h2>Tours from Phoenix vs a tour from Flagstaff</h2>
{table(['', 'Bus tour from Phoenix', 'Self-drive from Phoenix', 'Stay in Flagstaff + TrekWest day tour'],
       [['Hours in a vehicle', '9 to 11', '7 to 8', '3 to 4 (and someone else is driving)'],
        ['Time at the rim', '3 to 4 hours', 'As long as you like, minus the drive back', 'About 6 hours, including a picnic lunch'],
        ['Group size', 'Often 40 to 50', 'Just you', 'Maximum 10'],
        ['Park fees', 'Usually included', '$35 per vehicle (plus the non-resident fee if it applies to you)', 'Included'],
        ['Best for', 'No car, one day only', 'Flexible, confident drivers', 'People who want the day to be the highlight, not the drive']])}
<h2>Driving tips for the I-17</h2>
<ul>
<li><strong>Fuel up in Phoenix or Camp Verde.</strong> There is a long gap with little between Camp Verde and Flagstaff.</li>
<li><strong>Elevation.</strong> You climb from 1,100 ft to 7,000 ft. Expect your car (and your lungs) to notice. Drink water.</li>
<li><strong>Winter.</strong> Flagstaff gets real snow. Check ADOT (az511.gov) before you go, and use the Williams / SR-64 route to the park if US-180 is icy.</li>
<li><strong>Sunday afternoons.</strong> Southbound I-17 back into Phoenix is slow from about 2 pm. Leave earlier or later.</li>
</ul>
{CTA_DAY}
{related([('/flagstaff-to-grand-canyon/', 'Flagstaff to the Grand Canyon: the 80-mile drive'), ('/grand-canyon-itinerary-1-2-3-days/', 'Grand Canyon itineraries: 1, 2 and 3 days'), ('/finding-your-basecamp-where-to-stay-when-visiting-grand-canyon/', 'Where to stay when visiting the Grand Canyon'), ('/grand-canyon-trip-cost/', 'How much a Grand Canyon trip costs')])}
""")

guide('sedona-to-grand-canyon', 'Sedona to the Grand Canyon: Day Trip, Drive and Tour Options',
      'Sedona to Grand Canyon: Day Trip, Drive & Tours | TrekWest',
      'Sedona to the Grand Canyon South Rim is about 115 miles and 2 to 2.5 hours through Oak Creek Canyon and Flagstaff. How to do it as a day trip, what to stop for, and your tour options.',
      'Getting here', '34b2c517-33c5-4097-a5c5-ef282bf2ffaf', 'Red sandstone canyon reflected in a still creek with fall leaves', 2, f"""
{tldr(['Sedona to Grand Canyon Village: about 115 miles / 185 km, 2 to 2.5 hours each way via SR-89A up Oak Creek Canyon, Flagstaff and US-180.',
       'A day trip is very doable: leave by 7:30 am and you have 5 to 6 hours at the rim.',
       'The drive up Oak Creek Canyon is one of the best in Arizona. Do it in daylight at least once.',
       'Flagstaff is on the way. Our small-group tours leave from there; ask us about a Sedona pickup for private tours.'])}
<h2>The route from Sedona</h2>
<p>Take <strong>SR-89A north</strong> out of Uptown Sedona. The road follows Oak Creek for 14 miles, then climbs the switchbacks to the rim of the Mogollon Plateau (stop at the Oak Creek Vista pull-out at the top; the Navajo and Hopi vendors there are worth your time). You arrive in Flagstaff after about 45 minutes to an hour. From Flagstaff, <strong>US-180 north-west</strong> runs 80 miles through ponderosa pine and open grassland to the South Entrance of the park. Total: 2 to 2.5 hours depending on how long you linger in the canyon.</p>
<p>In winter, if 89A through Oak Creek is icy, take SR-179 south to I-17 and go up the interstate instead. It adds about 20 minutes.</p>
<h2>Sedona to Grand Canyon day trip: a realistic timeline</h2>
<ul>
<li><strong>7:30 am</strong> leave Sedona. <strong>8:30</strong> coffee in Flagstaff. <strong>10:00</strong> at the South Rim.</li>
<li><strong>10:00 to 3:30</strong> Mather Point, the Rim Trail to the Village, lunch, then the drive east along Desert View Drive to the Watchtower (25 miles, with the best overlooks in the park).</li>
<li><strong>3:30</strong> leave from Desert View. You can return via Cameron and US-89 south to Flagstaff, which makes a loop and passes the Little Colorado River Gorge. Back in Sedona by 6:30 pm.</li>
</ul>
<p>If you want sunset at the canyon (and you should, <a href="/why-book-a-grand-canyon-sunset-tour/">here is why</a>), accept a late night, or stay in Flagstaff or Tusayan instead.</p>
<h2>Your options for getting there</h2>
{table(['', 'Self-drive', 'Large bus tour from Sedona', 'TrekWest small-group tour (from Flagstaff)', 'TrekWest private tour'],
       [['Hours in the vehicle', '4.5 to 5', '5 to 6', '3 to 3.5 from Flagstaff', 'Depends on pickup; we can plan around Sedona'],
        ['Group size', 'You', 'Often 25 to 50', 'Maximum 10', 'Your group only'],
        ['Park fee, lunch', 'You pay ($35 per vehicle)', 'Usually included', 'Included: park fee, Route 66 café picnic', 'Included'],
        ['Guide', 'Audio app, if you download one', 'Driver-guide on a microphone', 'Local guide, walks with you at every stop', 'Your own guide, your pace'],
        ['Best for', 'Confident drivers who want flexibility', 'Lowest price per seat', 'Couples, small families, friends', 'Families, special occasions, hikers']])}
{PICKUP}
<h2>Two days are better than one</h2>
<p>Our favourite version: drive up Oak Creek Canyon mid-morning, hike <a href="/old-caves-crater-flagstaff-volcano-hike/">Old Caves Crater</a> or wander downtown Flagstaff, sleep in Flagstaff, and take the canyon tour the next day rested and early. Then, if you have a third day, <a href="/sycamore-canyon-parsons-trail-hike/">Sycamore Canyon</a> gives you Sedona-style red rock without the Sedona crowds on your way back south.</p>
{CTA_DAY}
{related([('/sedona-tours-guide/', 'Sedona tours without a Jeep'), ('/sedona-hiking-guide/', 'Sedona hiking for first-timers'), ('/grand-canyon-itinerary-1-2-3-days/', 'Grand Canyon itineraries: 1, 2 and 3 days'), ('/grand-canyon-horseshoe-bend-antelope-canyon-one-trip/', 'Grand Canyon, Horseshoe Bend and Antelope Canyon in one trip?')])}
""")

guide('flagstaff-to-grand-canyon', 'Flagstaff to the Grand Canyon: The 80-Mile Drive and How to Do It Right',
      'Flagstaff to Grand Canyon: Distance, Drive & Tours | TrekWest',
      'Flagstaff to the Grand Canyon South Rim is 80 miles and about 1.5 hours on US-180. Routes, winter driving, what to see on the way, and why Flagstaff is the best base for the canyon.',
      'Getting here', 'panograndcanyon', 'Two guests at a Grand Canyon overlook watching the Colorado River', 3, f"""
{tldr(['Flagstaff to Grand Canyon Village: 80 miles / 130 km, about 1 hour 30 minutes via US-180 and SR-64.',
       'The Williams route (I-40 west, then SR-64 north) is 10 minutes longer but plowed first in winter.',
       'Flagstaff is the best base: more hotels and restaurants than Tusayan, cooler than Phoenix, and under 90 minutes from the rim.',
       'Our day tours leave Flagstaff at 8 am and have you back by about 5:30 pm with park fees, lunch and the driving handled.'])}
<h2>The drive</h2>
<p>Head north-west out of Flagstaff on <strong>US-180</strong> (Humphreys Street becomes Fort Valley Road). You pass the Museum of Northern Arizona and the Arizona Snowbowl turn-off, climb through ponderosa pine with the San Francisco Peaks on your right, then drop onto open grassland for the last 30 miles to Valle. At Valle turn right on <strong>SR-64</strong> for the final 30 miles to Tusayan and the South Entrance. On a quiet morning it is 1 hour 20 minutes; allow 1 hour 45 minutes in summer when the entrance queue builds after 10 am.</p>
<p><strong>Winter alternative:</strong> I-40 west 30 miles to Williams, then SR-64 north 60 miles. ADOT keeps the interstate and SR-64 clear first. Check <a href="https://az511.gov" rel="noopener" target="_blank">az511.gov</a> before you leave if snow is forecast.</p>
<h2>Why we think Flagstaff beats staying at the canyon</h2>
<ul>
<li><strong>Choice.</strong> Tusayan has a handful of hotels and chain restaurants, all at a premium. Flagstaff has a historic downtown, dozens of restaurants, breweries and every price of hotel. <a href="/finding-your-basecamp-where-to-stay-when-visiting-grand-canyon/">Our basecamp guide</a> goes through the trade-offs.</li>
<li><strong>Other days.</strong> Sedona, Walnut Canyon, Wupatki and Sunset Crater, Meteor Crater and <a href="/flagstaff-arizonas-best-day-hikes/">excellent day hikes</a> are all within an hour.</li>
<li><strong>The price.</strong> Park entrance ($35 per vehicle) and the drive are the only extra costs, and on our tours both are covered.</li>
</ul>
<h2>Drive yourself or take a tour?</h2>
<p>Driving yourself is easy and the road is good. What you lose is the knowledge: which overlooks are worth the stop (and which are three parking lots looking at the same view), where the quiet picnic spots are, what the rock layers are telling you, where the condors have been roosting this week. A guide also solves the summer problem of the Village parking lots being full by 10 am.</p>
<p>Our <a href="/grand-canyon-day-tour-from-flagstaff/">Grand Canyon day tour from Flagstaff</a> picks up at your hotel at 8 am, caps at 10 guests, includes the park fee and a Route 66 café picnic lunch, and spends about six hours in the park across the Village, the Rim Trail and the Desert View overlooks. If you are staying in Williams, the <a href="/grand-canyon-day-tour-from-williams/">Williams departure</a> does the same loop.</p>
{PICKUP}
<h2>Worth a stop on the way</h2>
<ul>
<li><strong>Museum of Northern Arizona</strong> (3 miles out of town): the best introduction to the geology and the Colorado Plateau peoples you are about to see.</li>
<li><strong>Kendrick Park</strong> meadow at dawn or dusk for elk.</li>
<li><strong>Valle:</strong> the Planes of Fame air museum and the Flintstones-era Bedrock City remnants, for the kids and the kitsch.</li>
</ul>
{CTA_DAY}
{related([('/phoenix-to-grand-canyon/', 'Phoenix to the Grand Canyon'), ('/things-to-do-grand-canyon-south-rim/', 'Things to do at the South Rim'), ('/grand-canyon-day-hikes-guide/', 'Grand Canyon day hikes'), ('/grand-canyon-with-kids/', 'The Grand Canyon with kids')])}
""")

guide('las-vegas-vs-flagstaff-grand-canyon', 'Las Vegas or Flagstaff? Choosing Your Base for the Grand Canyon',
      'Las Vegas vs Flagstaff as a Grand Canyon Base | TrekWest',
      'From Las Vegas, the real Grand Canyon (the South Rim) is 4.5 hours away; the West Rim Skywalk is 2.5 hours but outside the national park. What each option gets you, and when Flagstaff is the smarter base.',
      'Compare your options', 'img-2416-1', 'Guests on a Grand Canyon overlook as the sun breaks through clouds', 10, f"""
{tldr(['Las Vegas to the South Rim (the national park you have seen in photos) is about 275 miles and 4.5 hours each way.',
       'Las Vegas to Grand Canyon West and the Skywalk is about 122 miles and 2 hours 15 minutes, but it is a different, narrower section on Hualapai tribal land, outside the national park.',
       'Flagstaff is 80 miles (1.5 hours) from the South Rim. If the canyon is the point of your trip, base there.',
       'A good hybrid: fly into Vegas, drive to Flagstaff (3.5 hours via US-93 and I-40), spend two nights, drive back.'])}
<h2>First, which Grand Canyon?</h2>
<p>This is the part most Las Vegas tour brochures skip. There are three places people mean when they say "Grand Canyon":</p>
{table(['', 'South Rim (Grand Canyon National Park)', 'Grand Canyon West (Skywalk)', 'North Rim'],
       [['From Las Vegas', '~275 mi, 4.5 h', '~122 mi, 2.25 h', '~265 mi, 4.5 h'],
        ['From Flagstaff', '80 mi, 1.5 h', '~250 mi, 5 h', '~210 mi, 4.5 h'],
        ['What it is', 'The national park: Mather Point, the Village, Desert View, Bright Angel Trail, the mile-deep views', 'A section of the canyon on the Hualapai Reservation with the glass Skywalk, outside the park', 'The quieter, higher, forested side of the park'],
        ['Open', 'All year', 'All year', 'Mid-May to mid-October for full services; limited after the 2025 Dragon Bravo fire'],
        ['Fees', '$35 per vehicle park entrance', 'Tribal admission, separate from the park and priced per person', '$35 per vehicle park entrance']])}
<p>The Skywalk is a legitimate attraction and the closest canyon experience to the Strip. But the photographs that made you want to come, the layered mile-deep immensity, the Colorado River as a green thread, the Watchtower at Desert View, are all South Rim. If you only see Grand Canyon West, you have not seen that.</p>
<h2>The Las Vegas day trip to the South Rim</h2>
<p>Bus tours from Las Vegas to the South Rim leave early (often 6 to 7 am) and return late (9 to 10 pm). Out of a 15-hour day you get roughly 3 hours at the rim, typically in the middle of the day when the light is flattest. Helicopter and plane tours shorten the travel but shorten the time at the rim too, and you are looking down at the canyon rather than standing in it. If a single day is genuinely all you have, a flight or a bus beats not going. Just know what you are trading.</p>
<h2>When Flagstaff is the better base</h2>
<p>If you have two or more nights to give the canyon, the maths changes completely. Fly into Las Vegas (cheap flights, lots of them), pick up a car, and drive <strong>US-93 south over the Hoover Dam bypass to Kingman, then I-40 east to Flagstaff</strong>: about 250 miles and 3.5 to 4 hours, with the Hoover Dam and Seligman's Route 66 strip as stops. Then:</p>
<ul>
<li>The South Rim is 1.5 hours away instead of 4.5. Sunset at the canyon becomes easy. So does a second visit.</li>
<li>You can take a <a href="/grand-canyon-day-tour-from-flagstaff/">small-group day tour</a> (max 10) with hotel pickup, or a <a href="/private-tours-grand-canyon-sunset-dark-sky-tour/">private sunset and dark-sky tour</a>, and leave the rental at the hotel.</li>
<li>Sedona, Wupatki, Walnut Canyon and the San Francisco Peaks are all day trips from Flagstaff.</li>
<li>Flagstaff hotels cost less than Strip hotels at the weekend, and a lot less than Tusayan.</li>
</ul>
<p>Phoenix is the other airport option: 2.5 hours to Flagstaff on I-17, and usually more flights. <a href="/phoenix-to-grand-canyon/">Our Phoenix guide</a> covers that drive.</p>
<h2>Our recommendation by trip length</h2>
<ul>
<li><strong>One day from Vegas, no car:</strong> a West Rim tour or a flight to the South Rim. Lower your expectations about time on the ground.</li>
<li><strong>One day from Vegas, with a car:</strong> leave at 5 am for the South Rim, come back via Williams and Route 66. Long but worth it.</li>
<li><strong>Two to four days:</strong> drive to Flagstaff. Give the canyon a full day with a guide and a second visit for sunset or a hike.</li>
</ul>
{CTA_DAY}
{related([('/grand-canyon-south-rim-vs-west-rim-vs-north-rim/', 'South Rim vs West Rim vs North Rim'), ('/grand-canyon-helicopter-vs-ground-tour/', 'Helicopter, van or on foot?'), ('/grand-canyon-itinerary-1-2-3-days/', 'Grand Canyon itineraries from Flagstaff'), ('/grand-canyon-trip-cost/', 'How much a Grand Canyon trip costs')])}
""")

guide('grand-canyon-helicopter-vs-ground-tour', 'Helicopter, Van or On Foot: How to Choose Your Grand Canyon Tour',
      'Grand Canyon Helicopter Tour vs Ground Tour vs Hike | TrekWest',
      'Thinking about a Grand Canyon helicopter tour? Here is an honest comparison with a guided rim tour and a day hike: what you see, how long you get, who each suits, and how to combine them.',
      'Compare your options', 'img-1468', 'Smiling TrekWest guide on a Grand Canyon rim outcrop', 11, f"""
{tldr(['Helicopter flights from the South Rim (Grand Canyon Airport, Tusayan) last roughly 25 to 50 minutes and must stay above the rim inside the national park; flights that land in the canyon only happen at Grand Canyon West.',
       'A guided ground tour gives you 5 to 6 hours at the rim, standing in the view, with a human who can explain it.',
       'A day hike below the rim is the only way to feel the scale with your own legs. It is also the one most people underestimate.',
       'They are not rivals. Fly for 30 minutes in the morning, spend the day with us, see sunset from the rim. That is a very good day.'])}
<h2>What each one is actually like</h2>
{table(['', 'Helicopter / airplane', 'Guided van tour (TrekWest)', 'Guided day hike (TrekWest)'],
       [['Time with the canyon', '25 to 50 min in the air', '5 to 6 hours at the rim', '5 to 6 hours, 3 of them below the rim'],
        ['What you see', 'The sweep: the whole width, the river, the North Rim, from above', 'The detail: overlooks, the Village history, geology up close, condors, the Watchtower', 'The inside: the walls rising around you, the rock layers at arm’s length, the silence'],
        ['Group size', '6 to 7 per aircraft', 'Max 10', 'Private group'],
        ['Physical demands', 'None; weight limits apply', 'Easy walking, up to you', 'Moderate; 3 to 6 miles with 1,000 to 2,000 ft of elevation back up'],
        ['Weather risk', 'Flights cancel in high wind or low cloud', 'Runs rain or shine', 'Runs in most conditions; we adjust the route'],
        ['Included', 'The flight', 'Park fee, Flagstaff pickup, picnic lunch, guide', 'Park fee, pickup, lunch, snacks, water, guide'],
        ['Price range', 'Mid to high per person for a short flight', '$199 adult / $149 child (day tour)', 'From $999 for 1 to 2 guests (private)']])}
<h2>The case for flying</h2>
<p>From the air you understand the geography in a way you cannot from the rim: how the Colorado River carved it, how the side canyons feed in, how far it runs to the north. For visitors with limited mobility, or who have one morning and want the single most dramatic half hour available, a flight is a fine choice. Book the earliest slot; the air is calmer and the light is better.</p>
<p>Two things to know. Inside Grand Canyon National Park, aircraft fly above the rim on fixed corridors; the "land at the bottom and have champagne" flights operate at Grand Canyon West, two and a half hours from Las Vegas and five hours from here. And a flight is a view, not a visit: no one explains what you are looking at, you cannot stop, and 30 minutes later it is over.</p>
<h2>The case for the ground</h2>
<p>Standing at Lipan Point as the shadows move across the Palisades, hearing why the rock changes colour at the Great Unconformity, watching a condor cruise at eye level: that is the experience people remember. A ground tour is also the one that works for everyone from toddlers to grandparents, in any weather, and includes a proper lunch. Ours is a maximum of 10 people with a guide who has been doing this for decades, which is a different thing from a 50-seat coach with a microphone.</p>
<h2>The case for the hike</h2>
<p>Walk 20 minutes down the South Kaibab Trail to <a href="/grand-canyon-bike-hike-day-tour/">Ooh Aah Point</a> and the canyon stops being a view and becomes a place. Go to Cedar Ridge or Skeleton Point on a <a href="/private-tour-guided-day-hikes-in-grand-canyon/">guided day hike</a> and you will have earned something most visitors never see. Read our <a href="/grand-canyon-day-hikes-guide/">day hikes guide</a> before you decide how far; the trail back up is the hard part.</p>
<h2>How to combine them</h2>
<ul>
<li><strong>Fly early, tour after.</strong> A 9 am flight from Tusayan, then we meet you in Tusayan at 10 and run the rest of the day. (Ask us; we can adjust pickup for private groups.)</li>
<li><strong>Tour one day, hike the next.</strong> Get your bearings with the overlooks, then go below the rim.</li>
<li><strong>Skip the flight, do sunset.</strong> If the budget covers one extra, <a href="/why-book-a-grand-canyon-sunset-tour/">the sunset tour</a> is the better upgrade for most people.</li>
</ul>
{CTA_DAY}
{related([('/grand-canyon-rafting-vs-rim-tour/', 'Rafting the Grand Canyon vs seeing it from the rim'), ('/how-to-choose-a-grand-canyon-tour-company/', 'How to choose a Grand Canyon tour company'), ('/las-vegas-vs-flagstaff-grand-canyon/', 'Las Vegas or Flagstaff as your base'), ('/grand-canyon-day-hikes-guide/', 'Grand Canyon day hikes')])}
""")

guide('grand-canyon-rafting-vs-rim-tour', 'Rafting the Grand Canyon vs Seeing It from the Rim: Which Trip Is Right for You?',
      'Grand Canyon Rafting Trips vs Rim Tours: Honest Guide | TrekWest',
      'Grand Canyon rafting trips range from a half-day float below Glen Canyon Dam to 18 days of whitewater. What each involves, how far ahead to book, and how to pair the river with a day at the rim.',
      'Compare your options', '556938485-10172586905480327-7804287271371365140-n', 'Backpacker beside the Colorado River at the bottom of the Grand Canyon', 12, f"""
{tldr(['"Grand Canyon rafting" covers three very different things: a calm half-day float from Glen Canyon Dam to Lees Ferry, a one-day whitewater run on Hualapai land at the far west end, and the classic 3 to 18-day expeditions through the whole canyon.',
       'The multi-day trips are the trip of a lifetime and book up a year or more ahead. The half-day float can be booked the same week.',
       'None of them show you what the rim shows you, and the rim shows you nothing of the river. Do both if you can.',
       'We run the rim side: small-group day tours, sunset tours and guided hikes from Flagstaff, 2 hours from Page and Lees Ferry.'])}
<h2>The three kinds of Grand Canyon rafting</h2>
{table(['', 'Half-day smooth-water float (Glen Canyon)', 'One-day whitewater (Grand Canyon West)', 'Multi-day expedition (Lees Ferry to Diamond Creek / Pearce Ferry)'],
       [['Where', 'Below Glen Canyon Dam to Lees Ferry, from Page, AZ', 'Diamond Creek to Pearce Ferry on the Hualapai Reservation, from Peach Springs', 'The whole national park section'],
        ['Length', '15 river miles, about 4 to 5 hours door to door', 'Full day; usually includes a helicopter or long drive out', '3 to 7 days motorised; 6 to 18 days oar or dory'],
        ['Rapids', 'None. Flat, cold, turquoise water under 1,000-ft walls; passes Horseshoe Bend from below', 'Several real rapids in the first hours, then calm', 'More than 80 named rapids, including Lava Falls and Crystal'],
        ['Who it suits', 'Everyone from 4 years up; non-swimmers fine', 'Fit adults and older kids who want a taste', 'People who can give the trip a week and sleep on sand for it'],
        ['Booking', 'Days to weeks ahead', 'Weeks to months', 'A year or more for most dates; cancellations do appear'],
        ['From Flagstaff', '2 hours to Page', '2.5 hours to Peach Springs', 'Put-in at Lees Ferry, 2.25 hours']])}
<h2>If you only have a day: float or rim?</h2>
<p>Different experiences for different people. The Glen Canyon float is gentle, beautiful and feels like a secret; the sandstone walls are the same Navajo Sandstone you see at Antelope Canyon, and you drift under Horseshoe Bend looking up at the people who drove there. But it is not the Grand Canyon proper, and you will not see the mile-deep layered views. For that you want to be on the South Rim, ideally with the afternoon light moving across the Palisades from Lipan Point or Desert View.</p>
<p>If you want to be on the water near Lees Ferry without a commercial float, our guides have written up two self-powered options: <a href="/kayak-horseshoe-bend-from-lees-ferry/">kayaking Horseshoe Bend from below with a backhaul</a> and <a href="/waterholes-canyon-by-kayak-from-lees-ferry/">Waterholes Canyon by kayak</a>.</p>
<h2>A plan that does both</h2>
<ol>
<li><strong>Day 1:</strong> <a href="/grand-canyon-day-tour-from-flagstaff/">Grand Canyon day tour</a> from Flagstaff. See the canyon from above, learn the geology, end at Desert View.</li>
<li><strong>Day 2:</strong> drive to Page (2 hours; stop at <a href="/glen-canyon-dam-overlook-page-arizona/">the dam overlook</a>), take the half-day float in the morning, Horseshoe Bend from the top at sunset.</li>
<li><strong>Day 3:</strong> Antelope Canyon with a Navajo guide, then back to Flagstaff via Cameron. <a href="/grand-canyon-horseshoe-bend-antelope-canyon-one-trip/">Here is how the logistics work</a>.</li>
</ol>
<h2>Before you book a multi-day trip</h2>
<ul>
<li>Commercial outfitters are licensed by the National Park Service; the park website lists them all. Motor trips are shorter and smoother; oar and dory trips are quieter and longer.</li>
<li>Summer is hot (often 100°F+ in the inner gorge) and busiest. April to May and September to October are the sweet spots.</li>
<li>Trips that start or end at Phantom Ranch involve hiking the Bright Angel Trail with a daypack: 9.5 miles and 4,400 ft. Train for it. <a href="/rim-to-river-day-grand-canyon-day-hike-what-when-how/">Our rim-to-river post</a> explains what that hike is really like.</li>
<li>Non-commercial (private) permits are a weighted lottery run each February for the following year.</li>
</ul>
{CTA_DAY}
{related([('/grand-canyon-helicopter-vs-ground-tour/', 'Helicopter, van or on foot?'), ('/grand-canyon-horseshoe-bend-antelope-canyon-one-trip/', 'Grand Canyon, Horseshoe Bend and Antelope Canyon in one trip'), ('/arizonas-best-water-hikes-a-guide-to-desert-oases/', 'Arizona’s best water hikes'), ('/grand-canyon-itinerary-1-2-3-days/', 'Grand Canyon itineraries')])}
""")

guide('grand-canyon-south-rim-vs-west-rim-vs-north-rim', 'South Rim vs West Rim vs North Rim: Which Grand Canyon Is Right for You?',
      'Grand Canyon South Rim vs West Rim (Skywalk) vs North Rim | TrekWest',
      'The South Rim, the West Rim Skywalk and the North Rim are hours apart and very different. Distances from Flagstaff, Las Vegas and Phoenix, seasons, crowds, fees and what each one is for.',
      'Compare your options', 'img-2895', 'Guests looking down to the Colorado River from a Grand Canyon lookout', 13, f"""
{tldr(['South Rim: the national park most people picture. Open all year, 80 miles from Flagstaff. This is where we run our tours.',
       'West Rim (Grand Canyon West): Hualapai tribal land with the Skywalk, 2.25 hours from Las Vegas and 5 hours from the South Rim. Not in the national park.',
       'North Rim: 1,000 ft higher, forested, one-tenth of the visitors, open roughly mid-May to mid-October. Services are limited after the 2025 Dragon Bravo fire; check nps.gov before planning around it.',
       'They are not interchangeable. Pick by what you want to see and where you are starting from.'])}
<h2>Side by side</h2>
{table(['', 'South Rim', 'West Rim / Skywalk', 'North Rim'],
       [['Part of Grand Canyon National Park?', 'Yes', 'No (Hualapai Reservation)', 'Yes'],
        ['Elevation', '~7,000 ft', '~4,800 ft', '~8,000 to 8,800 ft'],
        ['From Flagstaff', '80 mi / 1.5 h', '~250 mi / 5 h', '~210 mi / 4.5 h'],
        ['From Las Vegas', '~275 mi / 4.5 h', '~122 mi / 2.25 h', '~265 mi / 4.5 h'],
        ['From Phoenix', '~230 mi / 3.5 to 4 h', '~250 mi / 4.5 h', '~350 mi / 6 h'],
        ['Open', 'All year', 'All year', 'Full season mid-May to mid-Oct; road closes with the first big snow or Dec 1'],
        ['Fee', '$35 per vehicle, 7 days (non-resident per-person fee may apply)', 'Tribal admission per person, separate from the park pass', '$35 per vehicle (same pass as South Rim)'],
        ['Visitors per year', '~4.5 to 5 million', 'Around 1 million', 'A few hundred thousand'],
        ['Signature sights', 'Mather Point, the Village and El Tovar, Bright Angel and South Kaibab trails, Desert View Watchtower', 'The glass Skywalk, Guano Point, Eagle Point, helicopter landings to the river', 'Bright Angel Point, Point Imperial, Cape Royal, aspen forest'],
        ['Best for', 'First visit; the classic views; families; hikers', 'A short trip from Las Vegas; the Skywalk itself', 'A second visit; summer heat escape; solitude']])}
<h2>South Rim: the one to see first</h2>
<p>Everything you have seen in photographs is here: the mile-deep layered walls, the Colorado River glinting far below, the 1930s stone architecture of Mary Colter, the trails that drop below the rim. It is also the most accessible: good roads, free shuttles, open 365 days, and 90 minutes from Flagstaff's hotels and restaurants. Yes, it is the busiest. Go early, go east along Desert View Drive, or go with someone who knows which overlooks the buses skip. <a href="/things-to-do-grand-canyon-south-rim/">Our South Rim guide</a> covers what to do with a day there.</p>
<h2>West Rim: closest to Las Vegas, and a different thing</h2>
<p>Grand Canyon West is run by the Hualapai Tribe and is a real canyon experience: the walls are about 4,000 ft here, the Skywalk is genuinely vertiginous, and it is the only place aircraft can land near the river. Be clear about what it is not: it is not the national park, your park pass does not work, and it is a 5-hour drive from the South Rim, so "we'll do both" is a two-day plan. If you are in Las Vegas for one day, it is the realistic option. If the Grand Canyon is the reason for your trip, drive on to Flagstaff. <a href="/las-vegas-vs-flagstaff-grand-canyon/">That comparison is here.</a></p>
<h2>North Rim: the quiet one, with a caveat</h2>
<p>Only 10 miles across the canyon from the Village but 212 miles by road, the North Rim is higher, cooler, wetter and wonderfully empty. The views from Cape Royal and Point Imperial look south across the whole canyon. The caveat: the July 2025 Dragon Bravo fire destroyed the historic Grand Canyon Lodge and much of the developed area, and the 2026 season has run with reduced services. The NPS notice for autumn 2026 lists the campground, store and fuel all closing by mid-October, with the nearest services at Jacob Lake, 45 miles north. Treat it as a day trip with a full tank and a packed lunch, and check <a href="https://www.nps.gov/grca" rel="noopener" target="_blank">nps.gov/grca</a> for the current status before you commit a day to the drive.</p>
<h2>Which one should you choose?</h2>
<ul>
<li><strong>First time, from anywhere in Arizona:</strong> South Rim. No contest.</li>
<li><strong>One day from Las Vegas, no car:</strong> West Rim.</li>
<li><strong>You have seen the South Rim and it is summer:</strong> North Rim, once it is fully reopened.</li>
<li><strong>You want a guide:</strong> that is us, on the South Rim, from Flagstaff and Williams, in groups of 10 or fewer.</li>
</ul>
{CTA_DAY}
{related([('/las-vegas-vs-flagstaff-grand-canyon/', 'Las Vegas or Flagstaff as your base'), ('/things-to-do-grand-canyon-south-rim/', 'Things to do at the South Rim'), ('/grand-canyon-trip-cost/', 'Grand Canyon costs and fees'), ('/international-park-entrance-fees-to-grand-canyon/', 'Park entrance fees for international visitors')])}
""")

guide('grand-canyon-railway-vs-tour-from-williams', 'Grand Canyon Railway vs a Small-Group Tour from Williams: Which Should You Book?',
      'Grand Canyon Railway vs Guided Tour from Williams | TrekWest',
      'The Grand Canyon Railway leaves Williams at 9:30 am and gives you about 3 hours 45 minutes at the rim. Here is how that compares with a guided small-group day from Williams, and how to combine the two.',
      'Compare your options', 'img-1344', 'Guests gathered around a spotting scope at a Grand Canyon overlook', 14, f"""
{tldr(['The Railway runs daily from Williams: depart 9:30 am, arrive at the rim 11:45, leave 3:30 pm, back 5:45 pm (an hour earlier in November and December). 2 hours 15 minutes each way.',
       'That gives you about 3 hours 45 minutes at the canyon, on foot, around the Village. The East Rim and Desert View are out of reach without a bus add-on.',
       'A guided van day from Williams gets you about 6 hours in the park, across the Village, the Rim Trail and the Desert View overlooks, in a group of 10 or fewer.',
       'The train is a lovely experience in its own right, especially for kids and rail fans. If the canyon is the priority, the van wins on time and ground covered.'])}
<h2>How the day compares</h2>
{table(['', 'Grand Canyon Railway', 'TrekWest day tour from Williams'],
       [['Departure / return', '9:30 am / 5:45 pm (Williams depot)', 'Morning pickup in the Williams area / back late afternoon'],
        ['Travel time', '2 h 15 min each way by train (65 miles)', 'About 1 hour each way by van (60 miles on SR-64)'],
        ['Time at the canyon', '~3 h 45 min', '~6 h'],
        ['Where you go', 'Grand Canyon Village: Mather Point, El Tovar, Rim Trail on foot; optional coach add-on for more', 'Village, Rim Trail, then 25 miles of Desert View Drive: Grandview, Moran, Lipan, Desert View Watchtower'],
        ['Guide', 'Entertainers on board; no guide at the rim unless you add a bus tour', 'A local guide with you all day, at every stop'],
        ['Group', 'Hundreds on the train; coach add-ons are large groups', 'Maximum 10'],
        ['Included', 'The train ride; classes of service vary', 'Park fee, Route 66 café picnic lunch, water, pickup'],
        ['Best for', 'Rail fans, young kids who love trains, non-drivers who want the journey itself', 'Anyone who wants the most canyon per day, with context']])}
<h2>What the train does well</h2>
<p>It is a genuinely charming ride: restored 1920s to 1950s cars, musicians moving through the carriages, a staged "train robbery" on the way home, and a steam locomotive on select dates. For children it is often the highlight of the holiday. The depot is in the middle of Williams, next to the Railway hotel, so the logistics are simple. If you are spending two days at the canyon, taking the train one day and a guided tour the other is a lovely pairing.</p>
<h2>Where it falls short</h2>
<p>Time. Of 8 hours 15 minutes door to door, less than half is at the canyon, and all of it is on foot around the Village unless you buy a coach add-on. The East Rim drive to the Watchtower, which has the overlooks most of our guests say were the best of the day, is 25 miles away. And arriving at 11:45 puts you at the rim in the flattest light of the day, leaving before the afternoon shadows start to work.</p>
<h2>The small-group alternative from Williams</h2>
<p>Our <a href="/grand-canyon-day-tour-from-williams/">Grand Canyon day tour from Williams</a> picks up in the Williams area, drives the hour up SR-64, and spends the day in the park with a guide who walks with you: the Village and its history, the Rim Trail, a Route 66 café picnic at a quiet overlook, and the full Desert View Drive to the Watchtower. Park fees are included. Groups are capped at 10, so questions get answered.</p>
<p>Staying in Williams for a few nights? It is a good base: the Route 66 strip, Bearizona on the edge of town, and <a href="/flagstaff-to-grand-canyon/">Flagstaff</a> 30 minutes east for restaurants and hikes.</p>
<p><a class="btn" href="/grand-canyon-day-tour-from-williams/">See the day tour from Williams</a></p>
{related([('/grand-canyon-with-kids/', 'The Grand Canyon with kids'), ('/things-to-do-grand-canyon-south-rim/', 'Things to do at the South Rim'), ('/how-to-choose-a-grand-canyon-tour-company/', 'How to choose a Grand Canyon tour company'), ('/grand-canyon-itinerary-1-2-3-days/', 'Grand Canyon itineraries')])}
""")

guide('grand-canyon-horseshoe-bend-antelope-canyon-one-trip', 'Grand Canyon, Horseshoe Bend and Antelope Canyon: Can You Do All Three in One Trip?',
      'Grand Canyon + Horseshoe Bend + Antelope Canyon: How to Plan It | TrekWest',
      'Yes, but not in one day. Distances between the South Rim, Page, Horseshoe Bend and Antelope Canyon, the booking rules for the slot canyons, and a two or three-day plan from Flagstaff that works.',
      'Compare your options', 'horseshoebend', 'Horseshoe Bend near Page, Arizona', 15, f"""
{tldr(['Grand Canyon South Rim to Page (Horseshoe Bend and Antelope Canyon) is about 135 miles and 2.5 hours via Desert View and Cameron.',
       'Antelope Canyon is on the Navajo Nation and can only be visited on a guided tour with an authorised operator. Book ahead, especially for midday light in Upper Antelope.',
       'Horseshoe Bend is a 1.5-mile round-trip walk from a paid City of Page car park, 5 minutes south of town. No booking needed.',
       'One-day "all three" tours exist from Las Vegas and Phoenix. They are 14 to 16 hours long and give each place about an hour. From Flagstaff, two days does it properly.'])}
<h2>The geography</h2>
{table(['Leg', 'Distance', 'Time'],
       [['Flagstaff to Grand Canyon Village (US-180)', '80 mi', '1.5 h'],
        ['Grand Canyon Village to Desert View', '25 mi', '45 min with stops'],
        ['Desert View to Page via Cameron (SR-64, US-89)', '110 mi', '2 h'],
        ['Page to Horseshoe Bend car park', '5 mi', '10 min'],
        ['Page to Antelope Canyon (Upper or Lower)', '5 to 8 mi', '15 min'],
        ['Page back to Flagstaff (US-89)', '135 mi', '2.25 h']])}
<p>Notice that Desert View, the eastern end of the South Rim, is on the way from the canyon to Page. That is the hinge the whole plan turns on.</p>
<h2>The booking rules you need to know</h2>
<ul>
<li><strong>Antelope Canyon</strong> (Upper and Lower, plus Canyon X and others) is Navajo Nation land. Entry is by guided tour only, with Navajo-owned operators, and a Navajo Parks permit fee is built into the price. Upper Antelope is the famous light-beam canyon (beams roughly late March to early October, around midday); Lower is narrower, involves ladders, and is usually cheaper and less crowded. Both sell out in season; book weeks ahead.</li>
<li><strong>Horseshoe Bend</strong> is a City of Page site with a per-vehicle parking fee, a graded 0.75-mile trail each way, and a railed viewing platform. Sunrise and late afternoon are best; midday the river is in shadow and the car park is full.</li>
<li><strong>Grand Canyon National Park</strong> charges $35 per vehicle for seven days. Non-US residents 16 and over currently pay an additional per-person fee unless they hold an annual pass; <a href="/international-park-entrance-fees-to-grand-canyon/">details here</a>.</li>
</ul>
<h2>The plan that works: two days from Flagstaff</h2>
<ol>
<li><strong>Day 1, Grand Canyon.</strong> Take the <a href="/grand-canyon-day-tour-from-flagstaff/">day tour</a> (we handle the park fee, lunch and the driving, and finish at Desert View) or drive yourself and end the day at the Watchtower. Sleep in Flagstaff, or push on to Page (2 hours from Desert View) if you have booked a morning slot canyon.</li>
<li><strong>Day 2, Page.</strong> Antelope Canyon tour late morning, lunch in Page, <a href="/glen-canyon-dam-overlook-page-arizona/">the dam overlook</a>, Horseshoe Bend from about 4 pm. Drive back to Flagstaff by 8 pm, or stay a second night.</li>
<li><strong>Day 3, optional.</strong> The half-day float from the dam to Lees Ferry (see <a href="/grand-canyon-rafting-vs-rim-tour/">our rafting guide</a>), or <a href="/kayak-horseshoe-bend-from-lees-ferry/">kayak Horseshoe Bend from below</a>.</li>
</ol>
<h2>Can we do it in one day?</h2>
<p>From Flagstaff, technically: leave at 6 am, two hours at the South Rim, Desert View, Cameron, a 1 pm Antelope slot, Horseshoe Bend at 4, home by 7:30. You will have driven 350 miles and spent 90 minutes at the Grand Canyon. If that is truly your only option, we would rather you did that than skipped the canyon. But the people who write to us afterwards wishing they had done it differently are almost always the one-day people.</p>
<p>If you would like us to build a <a href="/private-tour-inquire-about-customized-private-tours/">private two-day version</a> with a guide the whole way, ask. We do this route often.</p>
{CTA_PRIV}
{related([('/grand-canyon-rafting-vs-rim-tour/', 'Rafting vs the rim'), ('/sedona-to-grand-canyon/', 'Sedona to the Grand Canyon'), ('/waterholes-canyon-by-kayak-from-lees-ferry/', 'Waterholes Canyon by kayak'), ('/grand-canyon-itinerary-1-2-3-days/', 'Grand Canyon itineraries')])}
""")

guide('how-to-choose-a-grand-canyon-tour-company', 'How to Choose a Grand Canyon Tour Company: 9 Questions to Ask Before You Book',
      'How to Choose a Grand Canyon Tour Company | TrekWest',
      'Big bus, Jeep, van or private guide? Nine questions that separate a great Grand Canyon tour from a long day in a coach: group size, what is included, where you stop, who your guide is, and the cancellation policy.',
      'Compare your options', 'van2', 'TrekWest tour van parked at a Grand Canyon viewpoint while guests look out', 16, f"""
{tldr(['Group size is the single biggest predictor of how your day feels. Ask for the maximum, not the average.',
       'Ask exactly which overlooks you stop at and for how long. "Grand Canyon South Rim" can mean one car park.',
       'Check what is included: park entrance ($35 per vehicle; more for non-residents), lunch, hotel pickup, water.',
       'Read reviews that mention the guide by name. A good guide is the product.'])}
<h2>1. How many people will be on my tour?</h2>
<p>Coaches carry 40 to 55. Mid-size buses carry 20 to 30. Vans carry 10 to 14. The difference is not comfort, it is time: a 50-person group takes 20 minutes to get off a bus and use the restroom, which across six stops is two hours of your day. Our tours are capped at 10 because that is the number at which a guide can still talk to everyone.</p>
<h2>2. Where, exactly, do we stop?</h2>
<p>Ask for the list. A good South Rim day should include the Village and Rim Trail <em>and</em> several of the Desert View Drive overlooks (Grandview, Moran, Lipan, Navajo Point, the Watchtower). Many large-group tours do Mather Point, the Village and lunch, then turn around. If the East Rim is not on the itinerary, you are missing the best views in the park.</p>
<h2>3. How long are we actually at the canyon?</h2>
<p>Subtract the driving. From Flagstaff or Williams you should get 5 to 6 hours in the park. From Phoenix, 3 to 4. From Las Vegas, often under 3. <a href="/las-vegas-vs-flagstaff-grand-canyon/">Where you start from matters more than which company you choose.</a></p>
<h2>4. What is included in the price?</h2>
<p>Park entrance, lunch, hotel pickup, water and snacks are the usual variables. Ask whether "lunch included" means a sandwich in a box on the bus or a sit-down picnic at an overlook. Ask whether gratuities are expected on top. Our day tours include the park fee, a Route 66 café picnic and Flagstaff pickup; non-resident park fees are the one thing that may be extra, and <a href="/international-park-entrance-fees-to-grand-canyon/">we explain that here</a>.</p>
<h2>5. Who is my guide, and what do they know?</h2>
<p>Driver-guides on large coaches are often seasonal. Ask how long the company's guides have worked at the canyon and whether they walk with you at the stops or stay with the vehicle. Look for reviews that name a guide and describe something they explained. That tells you more than a star rating.</p>
<h2>6. Jeep, van, bus or private car?</h2>
{table(['', 'Open Jeep / 4x4', 'Large coach', 'Small van (TrekWest)', 'Private'],
       [['Typical group', '6 to 8', '40 to 55', 'Max 10', 'Your party'],
        ['Good for', 'Short off-road scenery rides near Sedona or Tusayan; fun for kids', 'Lowest price per seat; long-distance days from Vegas or Phoenix', 'Full day at the canyon with a guide who can actually answer questions', 'Flexibility, special occasions, hikers, photographers'],
        ['Watch for', 'Wind, dust, sun; limited time at viewpoints; not a full canyon day', 'Little time at the rim; fixed stops; restroom queues', 'Fewer departures than coaches; book ahead in season', 'Price per person is higher for couples']])}
<h2>7. What happens if the weather turns?</h2>
<p>The canyon is spectacular in snow and after storms; a company that cancels at the first cloud is protecting its schedule, not your day. Ask about their policy. Ours: tours run rain or shine; if <em>we</em> cancel for hazardous roads or closures, you get a 100% refund.</p>
<h2>8. Are they a permitted operator?</h2>
<p>Commercial tours inside Grand Canyon National Park operate under a Commercial Use Authorization from the National Park Service. Reputable companies will say so on their site (we are an authorised permittee; it is in our footer). Operators on Hualapai or Navajo land hold tribal permits instead.</p>
<h2>9. Does the price make sense for what you get?</h2>
<p>A $70 seat on a 50-person coach from Las Vegas and a $199 seat on a 10-person van from Flagstaff are not the same product, any more than a motel and a boutique inn are. Work out the cost per hour at the rim, and the cost of the day you will remember.</p>
{CTA_DAY}
{related([('/grand-canyon-helicopter-vs-ground-tour/', 'Helicopter, van or on foot?'), ('/grand-canyon-trip-cost/', 'How much a Grand Canyon trip costs'), ('/frequently-asked-questions/', 'Our FAQs, including the cancellation policy'), ('/our-guides-the-trekwest-story/', 'Meet our guides')])}
""")

# ------------------------------------------------------------------ PLAN YOUR VISIT
guide('things-to-do-grand-canyon-south-rim', 'Things to Do at the Grand Canyon South Rim: A Guide’s List',
      'Things to Do at the Grand Canyon South Rim (Guide’s Picks) | TrekWest',
      'The best things to do at the Grand Canyon South Rim, ranked by people who go every day: the overlooks worth stopping for, the Village, walks below the rim, Desert View, sunset spots and what to skip.',
      'Plan your visit', 'img-1295', 'Family pointing out the view with their TrekWest guide at a Grand Canyon overlook', 20, f"""
{tldr(['With one day: Mather Point early, the Rim Trail through the Village, a short walk below the rim, then Desert View Drive to the Watchtower for the afternoon light.',
       'The East Rim overlooks (Grandview, Moran, Lipan, Navajo Point) are the best views in the park and the ones most day-trippers never reach.',
       'Sunset from Hopi, Mohave or Lipan Point is the finest free thing in Arizona.',
       'Skip: driving between the Village car parks in summer. Walk or take the free shuttles.'])}
<h2>The overlooks, in the order we would do them</h2>
<ol>
<li><strong>Mather Point.</strong> The first view, five minutes from the Visitor Center. Go before 9 am or after 4 pm; at midday it is a scrum. It is still worth it.</li>
<li><strong>The Rim Trail, Mather Point to the Village (2.5 miles, flat, paved).</strong> Yavapai Point and the Geology Museum (look at the relief model, then look at the real thing), then Trail of Time, where every metre is a million years. Shuttles bring you back.</li>
<li><strong>Grand Canyon Village.</strong> El Tovar (1905), Hopi House, Lookout Studio and Kolb Studio: Mary Colter's stone buildings on the very edge. Have a coffee on the El Tovar porch. Watch the mule trains come up Bright Angel.</li>
<li><strong>Hermit Road overlooks (west).</strong> Hopi Point for sunset, Mohave for the river and Hermit Rapid, The Abyss for vertigo. Private cars are banned March to November; take the red shuttle or walk the Rim Trail.</li>
<li><strong>Desert View Drive (east, 25 miles).</strong> Grandview Point (the widest view), Moran Point (the red layers Thomas Moran painted), Lipan Point (the river, the Unkar Delta, the best sunset on the East Rim), Navajo Point and the <strong>Desert View Watchtower</strong>, Colter's 70-ft stone tower with Hopi murals inside. Climb it.</li>
</ol>
<h2>Walk below the rim, even a little</h2>
<p>The canyon changes the moment you drop below the edge. Two easy tasters: <strong>Bright Angel Trail to the first tunnel</strong> (10 minutes down) and <strong>South Kaibab Trail to Ooh Aah Point</strong> (0.9 miles down, 600 ft, 45 minutes to an hour back up). Carry water, start early in summer, and remember that down is optional and up is mandatory. <a href="/grand-canyon-day-hikes-guide/">Our day hikes guide</a> covers the longer options.</p>
<h2>Things worth your time</h2>
<ul>
<li><strong>Ranger programmes.</strong> Free, daily, listed at the Visitor Center. The geology and condor talks are excellent.</li>
<li><strong>The condors.</strong> California condors (9-ft wingspan) roost near the Village and Lookout Studio. Ask a ranger or your guide where they have been this week.</li>
<li><strong>Tusayan Ruin and Museum</strong> on Desert View Drive: an 800-year-old Ancestral Puebloan village, usually empty.</li>
<li><strong>Sunset.</strong> Hopi Point is the classic (and crowded); Lipan Point faces the right way and has a tenth of the people. <a href="/why-book-a-grand-canyon-sunset-tour/">Why we think sunset is non-negotiable.</a></li>
<li><strong>Stargazing.</strong> The park is an International Dark Sky Park. Even from the Village car park the Milky Way is astonishing on a moonless night.</li>
<li><strong>The bike paths.</strong> The Greenway Trail from the Visitor Center to Hermit Road is paved and car-free. <a href="/grand-canyon-bike-hike-day-tour/">Our e-bike and hike day</a> rides it.</li>
</ul>
<h2>Things to skip (or at least not pay for)</h2>
<ul>
<li>Driving lot to lot in the Village in summer. Park once, walk and use the shuttles.</li>
<li>The IMAX in Tusayan, unless it is raining. The real thing is 10 minutes away.</li>
<li>Trying to "see the river" from Mather Point. You can glimpse it; go to Lipan, Mohave or Desert View for a proper look.</li>
</ul>
<h2>How we fit it into a day</h2>
<p>Our <a href="/grand-canyon-day-tour-from-flagstaff/">Grand Canyon day tour</a> does most of this list in one 8 am to 5:30 pm day: hotel pickup in Flagstaff, the Village and Rim Trail on foot, a Route 66 café picnic at a quiet overlook, and the full Desert View Drive with the Watchtower, in a group of 10 or fewer, with a guide who has been explaining these rocks for decades. Park fees included.</p>
{CTA_DAY}
{related([('/grand-canyon-day-hikes-guide/', 'Grand Canyon day hikes'), ('/grand-canyon-with-kids/', 'The Grand Canyon with kids'), ('/grand-canyon-itinerary-1-2-3-days/', 'Grand Canyon itineraries'), ('/grand-canyon-south-rim-vs-west-rim-vs-north-rim/', 'South Rim vs West Rim vs North Rim')])}
""")

guide('grand-canyon-day-hikes-guide', 'Grand Canyon Day Hikes: Bright Angel, South Kaibab and the Rim Trail (and When to Go Guided)',
      'Grand Canyon Day Hikes: Trails, Distances & Guided Options | TrekWest',
      'The best Grand Canyon day hikes from the South Rim with honest distances and elevation: Rim Trail, Ooh Aah Point, Cedar Ridge, Skeleton Point, 3-Mile Resthouse and Havasupai Gardens. Plus when a guided hike is worth it.',
      'Plan your visit', 'kaibabtrailhikinggrandcanyon', 'Hiker on a ledge above the Grand Canyon on the South Kaibab Trail', 21, f"""
{tldr(['Every hike below the rim is uphill on the way back, at 7,000 ft, often in heat. Plan on taking twice as long to come up as you took going down.',
       'Best short taster: South Kaibab to Ooh Aah Point (1.8 miles round trip, 600 ft). Best half day: Cedar Ridge (3 miles, 1,100 ft) or Bright Angel to 3-Mile Resthouse (6 miles, 2,100 ft).',
       'Do not attempt rim to river and back in a day in summer. The park says so with signs, and the rangers mean it.',
       'A guided hike is worth it if you want to go further than you would alone, want the geology explained, or are hiking with mixed abilities.'])}
<h2>The trails, from easy to hard</h2>
{table(['Hike', 'Round trip', 'Elevation to regain', 'Time', 'Water on trail?', 'Notes'],
       [['Rim Trail, Mather Point to the Village', '2.5 mi one way', 'Nearly flat', '1 to 1.5 h', 'Yes, at several points', 'Paved; shuttles back; the Trail of Time geology walk'],
        ['Rim Trail west, Village to Hermits Rest', '7.8 mi one way', 'Gentle', '3 to 4 h', 'Yes', 'Shuttle back from any stop; Hopi and Mohave Points'],
        ['South Kaibab to Ooh Aah Point', '1.8 mi', '600 ft', '1 to 1.5 h', 'No', 'The best view per step in the park; no shade'],
        ['South Kaibab to Cedar Ridge', '3 mi', '1,100 ft', '2 to 3 h', 'No', 'Toilets at Cedar Ridge; our guided day hike turnaround'],
        ['Bright Angel to 1.5-Mile Resthouse', '3 mi', '1,100 ft', '2 to 3 h', 'Seasonal (May to Oct)', 'Shade in the morning; the mule route'],
        ['South Kaibab to Skeleton Point', '6 mi', '2,000 ft', '4 to 6 h', 'No', 'First proper view of the river; strong hikers only in summer'],
        ['Bright Angel to 3-Mile Resthouse', '6 mi', '2,100 ft', '4 to 6 h', 'Seasonal', 'Good turnaround for a long half day'],
        ['Bright Angel to Havasupai Gardens', '9 mi', '3,000 ft', '6 to 9 h', 'Yes (all year at the Gardens)', 'Formerly Indian Garden; cottonwood shade; a full day, not for summer'],
        ['Rim to river and back', '16 to 19 mi', '4,400 to 4,800 ft', '10 to 14 h', 'Seasonal', 'Not recommended as a day hike. Read our post before you even think about it']])}
<h2>South Kaibab or Bright Angel?</h2>
<p><strong>South Kaibab</strong> follows a ridge, so the views are open and enormous from the first switchback. It has no water and almost no shade, and the trailhead is shuttle-only (no private cars). <strong>Bright Angel</strong> follows a side canyon, so it has shade in the morning, seasonal water, resthouses and more people. For a short hike with the best views, Kaibab. For a longer day in summer, Bright Angel. Many experienced hikers go down Kaibab and up Bright Angel when they do the full rim-to-river; <a href="/rim-to-river-day-grand-canyon-day-hike-what-when-how/">here is what that actually involves</a>.</p>
<h2>What people get wrong</h2>
<ul>
<li><strong>Time.</strong> Going down feels easy, and the canyon keeps pulling you. Set a turnaround time, not a turnaround point, and stick to it.</li>
<li><strong>Water and salt.</strong> At least a litre per hour in summer, plus salty snacks. The park treats more heat casualties than falls. <a href="/packing-snacks-for-your-hike-think-like-an-astronaut/">Pack like an astronaut.</a></li>
<li><strong>Season.</strong> April to May and late September to November are ideal. June to early September, be below the rim only before 10 am or after 4 pm. Winter brings ice on the top mile; microspikes are essential from December to March.</li>
<li><strong>Altitude.</strong> You start at 7,000 ft. If you flew in from sea level yesterday, choose a shorter hike today.</li>
<li><strong>Mules.</strong> Step to the inside (uphill) side of the trail, stand still, and do as the wrangler says.</li>
</ul>
<h2>When a guided hike makes sense</h2>
<p>You do not need a guide to walk to Ooh Aah Point. You might want one if you would like to go to Cedar Ridge or Skeleton Point and come back feeling great rather than wrecked; if you want someone reading the rock layers as you pass through them; if your group has mixed fitness; or if you simply want the logistics (the shuttle-only trailhead, the pickup, the water, the lunch, the timings) handled.</p>
<p>Our <a href="/private-tour-guided-day-hikes-in-grand-canyon/">private guided day hike</a> leaves Flagstaff at 8 am, hikes South Kaibab to Cedar Ridge with a long picnic stop, and has you back by 5:30 pm with your legs still working. The <a href="/grand-canyon-bike-hike-day-tour/">e-bike and hike day</a> combines the rim Greenway on bikes with the Ooh Aah Point walk and a picnic there. And if you want to go further, <a href="/private-tour-inquire-about-customized-private-tours/">talk to us</a>.</p>
<p><a class="btn" href="/private-tour-guided-day-hikes-in-grand-canyon/">See the guided day hike</a></p>
{related([('/things-to-do-grand-canyon-south-rim/', 'Things to do at the South Rim'), ('/flagstaff-arizonas-best-day-hikes/', 'Flagstaff’s best day hikes'), ('/grand-canyon-helicopter-vs-ground-tour/', 'Helicopter, van or on foot?'), ('/sedona-hiking-guide/', 'Sedona hiking for first-timers')])}
""")

guide('grand-canyon-trip-cost', 'How Much Does a Grand Canyon Trip Cost? Fees, Tours and What’s Included',
      'Grand Canyon Trip Cost: Park Fees, Tours & Budget | TrekWest',
      'What a Grand Canyon visit really costs in 2026: the $35 vehicle entrance fee, the non-resident surcharge, parking, lodging in Flagstaff vs the park, food, and what a guided tour includes so you can compare fairly.',
      'Plan your visit', 'lunch', 'Picnic lunch set on a rock with the Grand Canyon behind', 22, f"""
{tldr(['Park entrance: $35 per private vehicle, valid 7 days; $20 per person on foot or bike; $30 per motorcycle. Cards only at the gate.',
       'Non-US residents aged 16 and over currently pay an additional $100 per person unless they hold an annual pass; the $250 non-resident America the Beautiful pass covers a family in one car.',
       'Lodging is the big variable: a Flagstaff hotel often costs half of Tusayan or the in-park lodges.',
       'A guided day tour at $199 per adult includes the park fee, lunch, pickup and about six hours with a guide. Compare like with like.'])}
<h2>Park fees (checked October 2026)</h2>
{table(['Item', 'Cost', 'Notes'],
       [['Private vehicle, 7 days', '$35', 'Driver and all passengers'],
        ['Motorcycle, 7 days', '$30', ''],
        ['Individual (walk, bike, shuttle), 7 days', '$20', 'Age 16 and over'],
        ['Non-resident surcharge', '$100 per person, 16+', 'Waived with an annual pass or America the Beautiful pass'],
        ['Grand Canyon annual pass', '$70', 'US citizens and residents'],
        ['America the Beautiful pass', '$80 resident / $250 non-resident', 'All federal sites for a year; the non-resident version pays for itself for a family of three'],
        ['Free entrance days 2026', '$0 for US residents', 'Several per year (e.g. Juneteenth, Veterans Day); the non-resident fee may still apply']])}
<p>Fees change; the NPS page is the source of truth. International visitors should read <a href="/international-park-entrance-fees-to-grand-canyon/">our explainer on the non-resident fee</a> before arriving at the gate, because it catches families by surprise. On our day tours the standard vehicle entrance is included; the per-person non-resident fee, where it applies, is the one item that may be charged separately (see the tour pages).</p>
<h2>Getting there</h2>
<ul>
<li><strong>Rental car:</strong> market rate, plus fuel. Flagstaff to the rim and back is about 160 miles.</li>
<li><strong>Parking:</strong> free inside the park, but the Village lots fill by mid-morning in summer.</li>
<li><strong>Shuttles inside the park:</strong> free.</li>
<li><strong>From Phoenix or Las Vegas:</strong> add 4 to 9 hours of driving per day. <a href="/phoenix-to-grand-canyon/">Phoenix guide</a>, <a href="/las-vegas-vs-flagstaff-grand-canyon/">Las Vegas guide</a>.</li>
</ul>
<h2>Where you sleep is the biggest cost decision</h2>
{table(['Base', 'Typical mid-season nightly range', 'Trade-off'],
       [['Inside the park (El Tovar, Bright Angel, Maswik, Yavapai)', 'High; books out 6 to 13 months ahead', 'You are there for sunrise and sunset. Limited dining'],
        ['Tusayan (park gate)', 'High for what you get', '10 minutes from the gate; chain hotels, few restaurants'],
        ['Williams', 'Moderate', 'Route 66 charm; 1 hour to the rim; the train'],
        ['Flagstaff', 'Lowest range, widest choice', '1.5 hours to the rim; real town with restaurants, breweries and hikes']])}
<p><a href="/finding-your-basecamp-where-to-stay-when-visiting-grand-canyon/">Our basecamp guide</a> goes deeper on this.</p>
<h2>Food</h2>
<p>In-park options run from the Maswik food court to the El Tovar dining room. Prices are resort-level. The sensible move is a packed lunch from Flagstaff: the picnic tables at Grandview and Lipan Point have the best views of any restaurant in Arizona. (Our tours include a Route 66 café picnic for exactly this reason.) Flagstaff dinners: <a href="/best-places-to-eat-in-flagstaff-arizona/">our list</a>.</p>
<h2>Tours: what the price actually buys</h2>
{table(['', 'Self-drive day', 'Large coach day tour', 'TrekWest small-group day tour'],
       [['Headline price', '$0 + car', 'Lower per seat', '$199 adult / $149 child (12 and under)'],
        ['Park entrance', '$35 per car, plus any non-resident fee', 'Usually included', 'Included'],
        ['Lunch', 'Bring it or pay park prices', 'Sometimes; often a boxed sandwich', 'Route 66 café picnic included'],
        ['Fuel and parking stress', 'Yours', 'None', 'None; hotel pickup in Flagstaff'],
        ['Guide', 'None', 'Driver on a microphone', 'Local guide with you at every stop; max 10 guests'],
        ['Time at the rim', 'Your call', '3 to 4 h from Phoenix or Vegas', 'About 6 h']])}
<p>Private tours start from $899 (sunset and dark sky, 1 to 2 guests), $999 (guided day hike) and $1,100 (hike and e-bike) and scale with group size; <a href="/private-guided-tours-from-flagstaff-williams-grand-canyon/">details here</a>. For a family of four, a private day often costs less per person than you expect once park fees, lunch and the second rental car are counted.</p>
<h2>A sample two-day budget for two, based in Flagstaff</h2>
<ul>
<li>Two nights in Flagstaff: moderate hotel rate x 2</li>
<li>Guided day tour for two: $398, park fee and lunch included</li>
<li>Second day self-drive to the rim for sunset: $35 entrance, fuel, picnic</li>
<li>Dinners and breakfasts in town</li>
</ul>
<p>Leave out the tour and add the park fee, lunch and a day of driving, and the saving is smaller than the headline suggests. Add it and the day is the one you will talk about.</p>
{CTA_DAY}
{related([('/international-park-entrance-fees-to-grand-canyon/', 'Park fees for international visitors'), ('/how-to-choose-a-grand-canyon-tour-company/', 'How to choose a tour company'), ('/finding-your-basecamp-where-to-stay-when-visiting-grand-canyon/', 'Where to stay'), ('/grand-canyon-itinerary-1-2-3-days/', 'Itineraries')])}
""")

guide('grand-canyon-itinerary-1-2-3-days', 'Grand Canyon Itineraries: 1, 2 and 3 Days from Flagstaff',
      'Grand Canyon Itinerary: 1, 2 or 3 Days from Flagstaff | TrekWest',
      'Hour-by-hour Grand Canyon itineraries for one, two and three days using Flagstaff as your base: the South Rim done properly, a hike below the rim, sunset, and add-ons to Sedona, Wupatki and Page.',
      'Plan your visit', 'img-2476', 'Two guests watching the sun set over the Grand Canyon from a rocky ledge', 23, f"""
{tldr(['One day: the full South Rim, Village to Desert View, with sunset if you can stay late.',
       'Two days: add a hike below the rim or the e-bike day, and a proper sunset.',
       'Three days: add Sedona and Oak Creek Canyon, or Wupatki and Sunset Crater, or Page.',
       'Base in Flagstaff throughout. Everything below is 1.5 hours or less from your hotel.'])}
<h2>One day: the South Rim, properly</h2>
<p><strong>Self-drive version.</strong> Leave Flagstaff by 7:30 am on US-180. Mather Point by 9. Walk the Rim Trail to the Village (2.5 miles) via Yavapai Geology Museum; shuttle back. Short walk down Bright Angel to the first tunnel. Picnic lunch at Grandview Point. Drive Desert View Drive stopping at Moran, Lipan and Navajo Points; climb the Watchtower. Either head home via Cameron and US-89 (a loop) or wait for sunset at Lipan Point and drive back in the dark (1.75 hours).</p>
<p><strong>Guided version.</strong> We pick you up at 8 am, and the <a href="/grand-canyon-day-tour-from-flagstaff/">day tour</a> covers the same ground with the park fee, the picnic and the parking handled, and a guide explaining what you are looking at. Back at your hotel around 5:30 pm, in time for dinner downtown.</p>
<h2>Two days: add depth</h2>
<ul>
<li><strong>Day 1:</strong> the one-day plan above, but skip sunset.</li>
<li><strong>Day 2, choose one:</strong>
  <ul>
  <li><a href="/grand-canyon-bike-hike-day-tour/">E-bike and hike day</a>: the car-free Greenway along the rim by e-bike, then South Kaibab to Ooh Aah Point for a picnic.</li>
  <li><a href="/private-tour-guided-day-hikes-in-grand-canyon/">Guided day hike</a> to Cedar Ridge for people who want to get properly below the rim.</li>
  <li>A slow morning in Flagstaff (<a href="/where-locals-love-to-eat-in-flagstaff-sosta-and-macys/">coffee at Macy's</a>, the Museum of Northern Arizona), then the <a href="/grand-canyon-sunset-star-gazing-tour/">sunset and stargazing tour</a> departing at 2 pm. This is the combination we would pick.</li>
  </ul></li>
</ul>
<h2>Three days: add the neighbourhood</h2>
<p>Days 1 and 2 as above, then one of:</p>
<ul>
<li><strong>Sedona and Oak Creek Canyon.</strong> Drive down SR-89A (45 minutes), hike West Fork or Cathedral Rock early, lunch in Sedona, back up the canyon in the afternoon light. <a href="/sedona-hiking-guide/">Sedona hiking guide</a>.</li>
<li><strong>Wupatki, Sunset Crater and the Painted Desert.</strong> The 35-mile loop road north-east of Flagstaff: an 1,000-year-old volcano, 800-year-old pueblos, and the red edge of the Navajo Nation. Half a day, little walking, almost no crowds. We run this as <a href="/private-grand-canyon-tour-east-rim-volcanoes-and-wupatki/">a private East Rim and volcanoes day</a> too.</li>
<li><strong>Page.</strong> Horseshoe Bend and Antelope Canyon, 2 hours north. <a href="/grand-canyon-horseshoe-bend-antelope-canyon-one-trip/">How to make that work.</a></li>
<li><strong>Flagstaff's own trails.</strong> <a href="/old-caves-crater-flagstaff-volcano-hike/">Old Caves Crater</a>, Walnut Canyon, or <a href="/best-places-to-see-fall-leaves-in-flagstaff/">the aspens</a> in October.</li>
</ul>
<h2>Seasonal notes</h2>
<ul>
<li><strong>Summer (June to August):</strong> be at the rim early; afternoon monsoon storms from July are dramatic and brief; hike only early or late.</li>
<li><strong>Autumn (September to October):</strong> the best season. Warm days, cool nights, aspens turning near Flagstaff.</li>
<li><strong>Winter (November to March):</strong> snow on the rim, empty overlooks, extraordinary light. Hermit Road opens to private cars. Bring layers and traction for icy paths.</li>
<li><strong>Spring (April to May):</strong> windy but lovely; the river trips start running; Havasupai Gardens water turns on.</li>
</ul>
{PICKUP}
{CTA_DAY}
{related([('/things-to-do-grand-canyon-south-rim/', 'Things to do at the South Rim'), ('/grand-canyon-day-hikes-guide/', 'Grand Canyon day hikes'), ('/grand-canyon-trip-cost/', 'What it all costs'), ('/finding-your-basecamp-where-to-stay-when-visiting-grand-canyon/', 'Where to stay')])}
""")

guide('grand-canyon-with-kids', 'The Grand Canyon with Kids: A Family Guide from People Who Take Families Every Week',
      'Grand Canyon with Kids: Family Tour & Planning Guide | TrekWest',
      'Visiting the Grand Canyon with children: the safe overlooks, the Junior Ranger programme, how far to walk below the rim, where to eat, how to handle altitude and heat, and why a small-group or private tour works well for families.',
      'Plan your visit', 'img-2384', 'Family of five posing on a rocky Grand Canyon overlook', 24, f"""
{tldr(['Most rim viewpoints are railed; many stretches of the Rim Trail are not. Hold hands near the edge and set a rule: no one climbs on rocks beyond the rail.',
       'The Junior Ranger booklet (free at the Visitor Center) turns the day into a quest and ends with a badge. Children love it.',
       'Below the rim: Bright Angel to the first tunnel, or South Kaibab to Ooh Aah Point for kids over 7 or 8. No further in summer.',
       'A small-group or private tour removes the hardest parts of the day for parents: parking, pacing, snacks and the "what is that?" questions.'])}
<h2>Safety first, without ruining the day</h2>
<p>The Grand Canyon is not fenced. The developed viewpoints (Mather, Yavapai, the Village, Desert View) have railings; the Rim Trail between them often does not, and the drop is real. Our rules with family groups: an adult between each child and the edge; no running on the Rim Trail; no climbing past any rail for a photo, ever. Children take this seriously when adults do. With those in place, the rim is a wonderful place for kids.</p>
<h2>What children actually enjoy here</h2>
<ul>
<li><strong>Junior Ranger.</strong> Pick up the booklet at the Visitor Center, complete the activities (different pages for different ages), attend one ranger talk, get sworn in with a badge. Budget two hours across the day.</li>
<li><strong>The Trail of Time.</strong> A walk along the rim where each metre is a million years, with rock samples you can touch. Best for 6 and up.</li>
<li><strong>Yavapai Geology Museum.</strong> The relief model and the floor-to-ceiling windows. Short, warm, has restrooms.</li>
<li><strong>Mule trains, condors, elk and squirrels.</strong> Do not feed the squirrels; they bite and carry plague. Yes, really.</li>
<li><strong>The Watchtower at Desert View.</strong> Climbing the spiral stairs past the Hopi murals is a highlight for most kids. Small children may need carrying on the stairs.</li>
<li><strong>A short way down.</strong> Being below the rim is the thing they will remember. Bright Angel to the first tunnel (10 minutes) for small ones; <a href="/grand-canyon-bike-hike-day-tour/">Ooh Aah Point</a> for strong walkers of 7 or 8 and up, with a picnic as the reward.</li>
</ul>
<h2>Altitude, heat, cold and sun</h2>
<p>The rim is at 7,000 ft; children coming from sea level may be tired or headachy on day one, so plan a gentle first day. In summer, shade is scarce and the sun is fierce: hats, sunscreen, and a litre of water per child per half day. In winter, the rim is cold and icy where the sun does not reach; proper footwear matters. <a href="/packing-snacks-for-your-hike-think-like-an-astronaut/">Our snack post</a> is written for hikers but applies doubly to children.</p>
<h2>Food</h2>
<p>In-park options are limited and expensive, and queues at midday are long. A picnic at Grandview or Lipan Point, with a table and a view, is the better choice, and the Maswik food court is the fallback. Our tours include a Route 66 café picnic with Arizona-made treats; we have yet to meet a child who turned it down.</p>
<h2>Why families like small-group and private tours</h2>
<p>A day at the canyon with children has a lot of moving parts: parking that is full by 10, shuttle queues, restroom timing, snack timing, the edge. On a <a href="/grand-canyon-day-tour-from-flagstaff/">10-person tour</a> most of that disappears, and your guide becomes the person who answers "why is it red?" for the fourth time with real enthusiasm. A <a href="/private-guided-tours-from-flagstaff-williams-grand-canyon/">private day</a> goes further: your pace, your stops, a nap in the van if it is needed, and a route built around what your children can do. Children 12 and under are $149 on the group day tours.</p>
<h2>Where to stay with kids</h2>
<p>Flagstaff, for the same reasons as everyone else, plus playgrounds, a lively downtown, and the Lowell Observatory (where Pluto was discovered) for an evening. <a href="/finding-your-basecamp-where-to-stay-when-visiting-grand-canyon/">Basecamp guide.</a></p>
{CTA_DAY}
{related([('/things-to-do-grand-canyon-south-rim/', 'Things to do at the South Rim'), ('/grand-canyon-railway-vs-tour-from-williams/', 'The Grand Canyon Railway vs a guided day'), ('/grand-canyon-itinerary-1-2-3-days/', 'Itineraries'), ('/frequently-asked-questions/', 'FAQs')])}
""")

# ------------------------------------------------------------------ SEDONA
guide('sedona-hiking-guide', 'Sedona Hiking for First-Timers: Trails, Timing and Guided Options',
      'Sedona Hiking Guide: Best Trails & Guided Hikes | TrekWest',
      'The best Sedona hikes for a first visit, with distances, parking realities and the Red Rock Pass: Cathedral Rock, Devil’s Bridge, Bell Rock, West Fork, Fay Canyon and Doe Mountain. Plus quieter red-rock alternatives and private guided days from Flagstaff.',
      'Sedona', '17fd6c51-5c45-47d7-a462-71fbeca8c748', 'Calm creek lined with tall grass and fall-coloured trees in northern Arizona', 30, f"""
{tldr(['Sedona trails are short, beautiful and crowded. Start by 7 am or go after 3 pm, and use the free Sedona Shuttle for Cathedral Rock, Dry Creek (Devil’s Bridge) and Soldier Pass; those trailheads are closed to cars at peak times.',
       'Best first hikes: Bell Rock Pathway (easy), Fay Canyon (easy), Doe Mountain (moderate, best view for effort), Cathedral Rock (short, steep scramble), West Fork of Oak Creek (shady, water, long).',
       'Buy a Red Rock Pass ($5 per day) or use an America the Beautiful pass at most trailheads.',
       'Want red rock without the crowds? Sycamore Canyon, 30 minutes west, is our guides’ answer.'])}
<h2>Before you set off</h2>
<ul>
<li><strong>Parking is the hard part.</strong> The Cathedral Rock, Dry Creek Vista (Devil’s Bridge) and Soldier Pass trailheads are served by the free <strong>Sedona Shuttle</strong> from park-and-ride lots (Thursday to Sunday for most of the year, more days in spring), and are closed to private vehicles on shuttle days. Check sedonashuttle.com. Other trailheads fill by 8 am in spring and autumn.</li>
<li><strong>Red Rock Pass.</strong> $5 a day or $15 a week at trailhead machines; an America the Beautiful pass also works at most sites.</li>
<li><strong>Heat and exposure.</strong> Sedona is 4,300 ft, hotter than Flagstaff, with little shade on the slickrock. Summer hikes are dawn hikes.</li>
<li><strong>Cairns, not trails.</strong> Several routes cross bare rock and are marked only by rock cairns or painted blazes. If you have not seen a cairn for 5 minutes, go back to the last one.</li>
</ul>
<h2>The hikes, in order of difficulty</h2>
{table(['Trail', 'Distance', 'Elevation', 'Time', 'What it is'],
       [['Bell Rock Pathway and Courthouse Butte Loop', '4 mi loop (or as short as you like)', '300 ft', '1.5 to 2.5 h', 'Easy, wide, big views of Bell Rock and Courthouse Butte; large lot off SR-179'],
        ['Fay Canyon', '2.4 mi out and back', '200 ft', '1 to 1.5 h', 'Gentle box canyon with a natural arch side trip; good with children'],
        ['Doe Mountain', '1.5 mi out and back', '400 ft', '1.5 h', 'Short switchbacks to a flat mesa top with a 360° view; the best effort-to-view ratio in Sedona'],
        ['Airport Loop', '3.3 mi loop', '400 ft', '1.5 to 2 h', 'Wraps the mesa above town; sunset views; parking is tiny'],
        ['Cathedral Rock', '1.2 mi out and back', '740 ft', '1 to 2 h', 'A steep slickrock scramble to the saddle; the most photographed view in Sedona; shuttle only at peak'],
        ['Devil’s Bridge via Dry Creek / Mescal', '4 to 6 mi out and back', '400 to 600 ft', '2 to 3.5 h', 'A natural sandstone arch you can walk out on; expect a queue for the photo'],
        ['Soldier Pass', '4.5 mi out and back', '600 ft', '2.5 to 3 h', 'Devil’s Kitchen sinkhole, the Seven Sacred Pools and the arch caves; shuttle only at peak'],
        ['West Fork of Oak Creek', 'Up to 7 mi out and back', '300 ft', '3 to 4 h', 'Shady canyon with a dozen creek crossings and 1,000-ft walls; 10 miles north of town on 89A; paid lot; glorious in October'],
        ['Bear Mountain', '5 mi out and back', '1,900 ft', '4 to 5 h', 'The hard one: steep, exposed, enormous views to the San Francisco Peaks; strong hikers only']])}
<h2>If you want red rock without the Sedona crowds</h2>
<p>Thirty minutes west of Sedona, past Cottonwood and Clarkdale, <a href="/sycamore-canyon-parsons-trail-hike/">Sycamore Canyon's Parsons Trail</a> follows a spring-fed creek between red walls as high as anything in Sedona, with a fraction of the people. In autumn the cottonwoods along Oak Creek and in Sycamore Canyon turn gold; <a href="/best-places-to-see-fall-leaves-in-flagstaff/">our fall colour post</a> has timing.</p>
<h2>Guided hiking in Sedona</h2>
<p>Sedona's famous tours are mostly vehicle tours, which are a different thing from hiking. If you would like a guide on foot, for the trail finding, the geology (these are the same rock layers you see at the Grand Canyon, just the top of the stack), the wildlife and the safety on exposed sections, we build <a href="/private-tour-inquire-about-customized-private-tours/">private guided days</a> from Flagstaff that can start in Sedona or Oak Creek Canyon and finish at a viewpoint for sunset. Tell us your group's fitness and we will suggest a route.</p>
{PICKUP}
{CTA_PRIV}
{related([('/sedona-tours-guide/', 'Sedona tours without a Jeep'), ('/sedona-to-grand-canyon/', 'Sedona to the Grand Canyon'), ('/flagstaff-arizonas-best-day-hikes/', 'Flagstaff’s best day hikes'), ('/arizonas-best-water-hikes-a-guide-to-desert-oases/', 'Arizona’s best water hikes')])}
""")

guide('sedona-tours-guide', 'Sedona Tours Without a Jeep: Red Rock Hikes, Scenic Drives and Private Days Out',
      'Sedona Tours: Jeep, Hiking, Scenic Drive or Private Guide? | TrekWest',
      'Sedona tours compared: the famous Jeep rides, guided hikes, the scenic drives you can do yourself (Red Rock Loop, Oak Creek Canyon, Schnebly Hill) and private guided days that pair Sedona with the Grand Canyon.',
      'Sedona', 'img-1632', 'Hiker standing beside a creek under red rock walls and golden fall leaves', 31, f"""
{tldr(['Sedona’s signature tours are open-air Jeep and 4x4 rides: 1.5 to 3 hours of bumpy fun on forest roads with big views. Great for kids and for anyone who cannot hike. Not a full day, and not a hike.',
       'The best scenery in Sedona is free: Red Rock Scenic Byway (SR-179), Oak Creek Canyon (SR-89A), Red Rock Loop Road and Airport Mesa at sunset.',
       'If you want to be on the trails with someone who knows them, book a guided hike, not a Jeep.',
       'A private day from Flagstaff can combine Oak Creek Canyon, a Sedona hike and sunset, or link Sedona and the Grand Canyon across two days.'])}
<h2>The honest menu of Sedona tours</h2>
{table(['', 'Jeep / 4x4 ride', 'Guided hike', 'Scenic drive (self)', 'Private guided day (TrekWest)'],
       [['Length', '1.5 to 3 h', '2 to 5 h', 'As long as you like', 'Full day'],
        ['What you get', 'Rough forest roads (Broken Arrow, Schnebly Hill, Soldier Pass), overlooks, a driver with stories', 'On the trail with a guide: route finding, geology, pacing, safety on slickrock', 'The views from the road and the big pull-outs', 'Oak Creek Canyon, a trail matched to your group, a picnic, sunset; or Sedona one day and the Grand Canyon the next'],
        ['Group', '6 to 10 per vehicle', 'Small', 'You', 'Your party'],
        ['Physical', 'None (bumpy)', 'Moderate', 'None', 'You choose'],
        ['Best for', 'Families with young kids, limited mobility, short on time', 'Walkers who want more than a viewpoint', 'Budget, flexibility', 'Couples and families who want a whole day designed around them']])}
<h2>The scenic drives you can do without a tour</h2>
<ul>
<li><strong>Red Rock Scenic Byway (SR-179, 7.5 miles).</strong> From the Village of Oak Creek into Sedona past Bell Rock, Courthouse Butte and the Chapel of the Holy Cross. Pull-outs everywhere. Do it in the morning with the sun behind you.</li>
<li><strong>Oak Creek Canyon (SR-89A north, 14 miles to the switchbacks).</strong> Slide Rock State Park, West Fork, the Oak Creek Vista at the top. The best drive in Arizona per mile, and the way to Flagstaff. <a href="/sedona-to-grand-canyon/">On to the Grand Canyon from here.</a></li>
<li><strong>Red Rock Loop Road (west Sedona, 11 miles, partly unpaved).</strong> Crescent Moon Picnic Site for the Cathedral Rock reflection at Red Rock Crossing.</li>
<li><strong>Schnebly Hill Road.</strong> The first mile is paved to a fine overlook; beyond that it is a rough road best left to the Jeeps and high-clearance vehicles.</li>
<li><strong>Airport Mesa</strong> at sunset. Tiny car park; walk up from the lower lot.</li>
</ul>
<h2>What a private day with us looks like</h2>
<p>We are a Flagstaff company, 45 minutes up Oak Creek Canyon from Sedona, and we build Sedona days for private groups rather than running a fixed Jeep loop. A typical version: pickup in the morning, the drive down Oak Creek Canyon with stops, a trail chosen for your group (Fay Canyon and Doe Mountain for families; Bear Mountain or West Fork for walkers), a picnic lunch, the Chapel and the Red Rock Scenic Byway in the afternoon, and sunset from Airport Mesa or back at the Oak Creek Vista. Or split it across two days with the <a href="/grand-canyon-day-tour-from-flagstaff/">Grand Canyon</a>: red rock one day, the big canyon the next, from one Flagstaff hotel.</p>
{PICKUP}
<h2>Things worth knowing before you book anything in Sedona</h2>
<ul>
<li><strong>Spring break and October</strong> are the busiest periods; roundabouts on SR-179 back up for an hour. Start early.</li>
<li><strong>The Sedona Shuttle</strong> is free and the only way into the Cathedral Rock and Devil’s Bridge trailheads on peak days.</li>
<li><strong>Vortex sites</strong> (Airport Mesa, Bell Rock, Cathedral Rock, Boynton Canyon) are also simply the best viewpoints; you do not need a specialist tour to visit them.</li>
<li><strong>Antelope Canyon and Horseshoe Bend</strong> are 2.75 hours north of Sedona; they are not a Sedona day trip. <a href="/grand-canyon-horseshoe-bend-antelope-canyon-one-trip/">Plan them from Flagstaff instead.</a></li>
</ul>
{CTA_PRIV}
{related([('/sedona-hiking-guide/', 'Sedona hiking for first-timers'), ('/sedona-to-grand-canyon/', 'Sedona to the Grand Canyon'), ('/sycamore-canyon-parsons-trail-hike/', 'Sycamore Canyon: red rock without the crowds'), ('/how-to-choose-a-grand-canyon-tour-company/', 'How to choose a tour company')])}
""")

# ------------------------------------------------------------------ write
pages = ROOT / 'src/pages'
for g in G:
    meta = {'kind': 'guide', 'title': g['title'], 'desc': g['desc'], 'h1': g['h1'], 'cat': g['cat']}
    (pages / f"{g['slug']}.html").write_text(f"<!--meta {json.dumps(meta, ensure_ascii=False)} -->\n{g['body'].strip()}\n")
    site['pages'][f"/{g['slug']}/"] = {'priority': 0.7, 'og': g['og'], 'ogalt': g['ogalt'], 'desc': g['desc'], 'date': DATE, 'rank': g['rank']}
json.dump(site, open(ROOT / 'src/site.json', 'w'), indent=1, ensure_ascii=False)
print('wrote', len(G), 'guides')
