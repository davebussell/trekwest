"""Turn the detailed @trekwesttours Instagram posts into blog articles (idempotent). Run from repo root."""
import json, re, html
man=json.load(open('src/img/manifest.json')); site=json.load(open('src/site.json'))
IG='https://www.instagram.com/trekwesttours/reel/'
CTA_PRIVATE='<p><strong>Want a local guide?</strong> TrekWest runs <a href="/private-guided-tours-from-flagstaff-williams-grand-canyon/">private tours</a> and <a href="/book-your-tour/">small-group Grand Canyon day tours</a> from Flagstaff and Williams. <a href="/contact-us/">Ask us about a custom day</a>.</p>'
def src(id,date): return f'<p class="small">Originally shared on Instagram <a href="{IG}{id}/" target="_blank" rel="noopener">@trekwesttours</a>, {date}.</p>'
P=[]
def post(slug,title,date,iso,cats,img,desc,body,ig,cta=CTA_PRIVATE):
    P.append(dict(slug=slug,title=title,date=date,iso=iso,cats=cats,img=img,desc=desc,body=body,ig=ig,cta=cta))

post('waterholes-canyon-by-kayak-from-lees-ferry','Waterholes Canyon: A Hidden Slot Canyon Only Reachable by Water','Oct 19, 2026','2026-10-19','Day Trips, Page',
 '556626191-10172586905765327-6579119463710531093-n',
 'How to reach Waterholes Canyon, a sandstone slot canyon near Lee’s Ferry that you can only get to by kayak, plus safety tips for flash floods.',
 '''<p>One of Arizona’s most beautiful slot canyons has no road to it. Waterholes Canyon cuts through sandstone along the Colorado River, about three miles upstream from Lee’s Ferry near Page, and the easy way in is by kayak.</p>
<h3>What you’ll see</h3>
<p>Towering red rock walls, narrow winding passages and soft light filtering down through the sandstone. It makes a memorable stop in the middle of a paddle.</p>
<h3>How to get there</h3>
<ol><li>Start at Lee’s Ferry and arrange a motorized kayak backhaul upstream toward Horseshoe Bend. <a href="https://www.instagram.com/kayak_horseshoe_bend/" target="_blank" rel="noopener">Kayak Horseshoe Bend</a> is one good option for the backhaul service.</li>
<li>Paddle back downstream. About three miles above Lee’s Ferry, pull your kayak onto a safe landing area.</li>
<li>Explore the canyon on foot.</li></ol>
<h3>Good to know</h3>
<ul><li>Bring plenty of water.</li><li>Wear shoes that suit hiking through sand and rock.</li><li>Check the weather across the wider area before you go. <strong>Never enter a slot canyon when flash flooding is possible</strong>, even if the sky above you is clear.</li></ul>
<p>Save this one for your next Northern Arizona road trip. If you’re building a Page and Horseshoe Bend itinerary, see our companion guide to <a href="/kayak-horseshoe-bend-from-lees-ferry/">kayaking Horseshoe Bend from the bottom</a>.</p>''','DeqaBxnATeI')

post('old-caves-crater-flagstaff-volcano-hike','Old Caves Crater: An Ancient Pueblo Hiding on a Volcano Near Flagstaff','Oct 18, 2026','2026-10-18','Flagstaff, Hiking',
 'img-2353-2','A free 2.5 to 3.5 mile hike up an extinct cinder cone to Sinagua cave dwellings, 15 minutes from downtown Flagstaff. Trail facts and directions.',
 '''<p>There is an archaeological site on top of a volcano just 15 minutes from downtown Flagstaff. Old Caves Crater is an extinct volcanic cinder cone with a collection of small caves that were once built into a Sinagua pueblo dating back to the 1300s. Archaeologists believe the settlement had roughly 70 to 80 rooms.</p>
<p>On the way up you get views of the San Francisco Peaks, Mount Elden and the surrounding volcanic landscape. It is a good workout with a little history and adventure thrown in.</p>
<h3>Trail facts</h3>
<ul><li><strong>Distance:</strong> about 2.5 to 3.5 miles round trip, depending on your route</li><li><strong>Elevation gain:</strong> about 500 to 650 feet</li><li><strong>Time:</strong> allow 1.5 to 2.5 hours</li><li><strong>Difficulty:</strong> moderate, with some loose volcanic cinders and uphill climbing</li><li><strong>Parking and entrance:</strong> both free, no permit required</li></ul>
<h3>Getting there</h3>
<p>From Flagstaff, take Highway 89 north to Silver Saddle Road. Turn right and drive about half a mile. The trailhead parking lot is on your left.</p>
<h3>Please protect it</h3>
<p>This is a protected archaeological site, and pottery fragments and other artifacts can still be found in the area. Leave everything exactly where you find it so future generations can experience it too.</p>''','DenyVX8ASJp')

post('sycamore-canyon-parsons-trail-hike','Sycamore Canyon: A Red Rock Hike Without the Sedona Crowds','Oct 17, 2026','2026-10-17','Hiking, Verde Valley',
 '34b2c517-33c5-4097-a5c5-ef282bf2ffaf','Parsons Trail #144 in Sycamore Canyon near Clarkdale: distance, difficulty, directions and local tips for a quieter red rock hike.',
 '''<p>Looking for one of Northern Arizona’s most beautiful hikes without the crowds of Sedona? Put Sycamore Canyon on your list. Just outside Clarkdale, Parsons Trail #144 leads into a red rock canyon of towering cliffs, cottonwood and sycamore trees, clear pools and a creek winding through the wilderness. It feels like a different Arizona.</p>
<h3>Hike details</h3>
<ul><li><strong>Trail:</strong> Parsons Trail #144</li><li><strong>Distance:</strong> about 7.5 to 8 miles round trip to Parsons Spring, though shorter hikes are well worth it</li><li><strong>Difficulty:</strong> easy to moderate, with rocky sections and creek crossings</li><li><strong>Best seasons:</strong> spring and fall</li><li><strong>Highlights:</strong> swimming holes, canyon walls, wildlife, shade trees and creek scenery</li></ul>
<h3>Directions</h3>
<p>From Cottonwood, follow signs toward Tuzigoot National Monument. Cross the Verde River bridge and turn left onto Sycamore Canyon Road (Forest Road 131). Follow it about 11 miles to Parsons Trailhead.</p>
<p><strong>The road is rough dirt and gravel.</strong> A high-clearance vehicle is strongly recommended, especially toward the end. Don’t drive it after heavy rain.</p>
<h3>Local tips</h3>
<ul><li>Download offline maps, because cell service is limited.</li><li>Bring plenty of drinking water and water shoes for the creek crossings.</li><li>Watch for flash floods and never enter the canyon when storms threaten.</li><li>There are no developed facilities at the trailhead.</li><li>Check road and trail conditions before you head out.</li></ul>
<p>Bring a camera and a picnic and enjoy the sound of running water beneath the canyon walls.</p>''','DeleKXmgeWp')

post('camp-verde-day-trip-from-flagstaff','Camp Verde: A Day Trip Worth Taking, Less Than an Hour from Flagstaff','Oct 16, 2026','2026-10-16','Day Trips, Verde Valley',
 '17fd6c51-5c45-47d7-a462-71fbeca8c748','Kayaking, pecan orchards, wine, antiquing, Montezuma Castle and more: a stop-by-stop day trip guide to Camp Verde, Arizona.',
 '''<p>Less than an hour from Flagstaff, Camp Verde packs in outdoor adventure, local wineries, pecan orchards, antique shops and small-town charm. Here are the stops we’d put on a day trip.</p>
<ul class="stops">
<li><strong>Kayak the Verde River.</strong> Paddle through beautiful scenery and watch for wildlife. Verde Adventures offers rentals and guided trips.</li>
<li><strong>Explore the pecan orchards.</strong> Take a scenic drive along Salt Mine Road to find local farms and pecan groves.</li>
<li><strong>Salt Mine Wine.</strong> Locally made wine in the countryside, at 536 W Salt Mine Road.</li>
<li><strong>Go antiquing.</strong> Hunt for vintage treasures at Sweet Pea Trading and other shops, 437 W Highway 260.</li>
<li><strong>Wingfield Bread Company.</strong> Artisan sourdough, pastries and fresh sandwiches at 564 S Main Street.</li>
<li><strong>Montezuma Castle.</strong> An ancient cliff dwelling at 2800 Montezuma Castle Road.</li>
<li><strong>Fort Verde State Historic Park.</strong> Arizona frontier history at 125 E Hollamon Street.</li>
<li><strong>Out of Africa Wildlife Park.</strong> A wildlife adventure at 3505 W Highway 260.</li>
<li><strong>Montezuma Well.</strong> A natural spring and ancient archaeological site near Rimrock.</li></ul>
<p>From lush riverbanks to vineyards and historic sites, Camp Verde is a side of Arizona many visitors miss. A reader also recommends the coffee at Thanks a Latte Café, a favorite stop for people driving up from Phoenix.</p>''','DeiqaoAgLiZ')

post('fossil-creek-arizona-waterfall-guide','Fossil Creek: How to Reach Arizona’s Turquoise Waterfall Swimming Holes','Oct 13, 2026','2026-10-13','Hiking, Water Hikes',
 'img-0382','Directions, permits, road conditions and safety tips for Fossil Creek, one of Arizona’s best swimming holes. Know before you go.',
 '''<p>Crystal-clear turquoise water, waterfalls and lush greenery tucked into rugged wilderness make Fossil Creek one of the best swimming holes in Arizona. It takes some planning to get there, so here is what to know first. For more places like this, see our guide to <a href="/arizonas-best-water-hikes-a-guide-to-desert-oases/">Arizona’s best water hikes</a>.</p>
<h3>Directions to the waterfall</h3>
<p>From Camp Verde, take I-17 Exit 287 and head east on Highway 260 toward Payson for about 10 miles. Turn right onto Fossil Creek Road (Forest Road 708) and follow the rugged dirt road about 14 miles to the Dixon Lewis Trailhead (formerly the Waterfall Trailhead). From the parking lot it is about a one-mile hike each way to the waterfall.</p>
<p><strong>Do not approach from Strawberry or Pine.</strong> The connecting road to the waterfall parking area is closed, and GPS directions can mislead you. Plan your route in advance.</p>
<h3>Know before you go</h3>
<ul><li><strong>4WD recommended.</strong> The road is rough, rocky and slow. High clearance is strongly recommended.</li>
<li><strong>Permits.</strong> Fossil Creek typically requires advance parking permits from April 1 through October 1, and they can sell out. Reserve the Dixon Lewis (Waterfall) Trailhead lot specifically, at <a href="https://www.recreation.gov/permits/4251919" target="_blank" rel="noopener">recreation.gov</a>.</li>
<li><strong>Limited parking.</strong> Only designated spaces are allowed, so confirm access before the long drive.</li>
<li><strong>Bring lots of water.</strong> The creek is not drinking water, and the heat, exposed trails and terrain can be dangerous. Pack snacks and sun protection too.</li>
<li><strong>Flash floods.</strong> Storms miles upstream can send floodwater through the canyon with little warning. Check the weather, avoid monsoon storms and move to higher ground if the water rises or turns muddy.</li>
<li><strong>Check conditions.</strong> Closures and rules change. Call the Fossil Creek information hotline at 928-226-4611 before you go.</li></ul>
<p>Is it worth it? Absolutely. Come prepared, respect the wilderness and pack out everything you bring in.</p>''','DeZ9HICyW-g')

post('kayak-horseshoe-bend-from-lees-ferry','Kayak Horseshoe Bend from the Bottom: A Lee’s Ferry Backhaul Guide','Oct 12, 2026','2026-10-12','Day Trips, Page',
 'horseshoebend','How to paddle the Colorado River around Horseshoe Bend from Lee’s Ferry with a motorboat backhaul, which outfitters to call, and what to bring.',
 '''<p>You can see Horseshoe Bend from the overlook, or you can float right around it. From Lee’s Ferry you explore the Colorado River beneath towering canyon walls, with ancient petroglyphs and hidden beaches along the way.</p>
<h3>How it works</h3>
<p>Book a kayak backhaul. A motorboat takes you and your kayak upstream toward Glen Canyon Dam, up to 15 miles. From there you paddle downstream at your own pace and finish right back where you parked. Choose a few hours, a full day or an overnight camping trip.</p>
<h3>Rentals and backhaul companies</h3>
<ul><li><strong>Kayak the Colorado:</strong> rentals and motorboat backhaul services</li><li><strong>Lee’s Ferry On The Fly:</strong> kayak rentals and customizable upstream drop-offs</li><li><strong>Wilderness River Adventures:</strong> backhaul for guests who bring their own watercraft</li><li><strong>Fly Fishing Specialties:</strong> group backhauls and kayak rentals</li></ul>
<p>Prefer not to paddle? Wilderness River Adventures also runs scenic half-day Horseshoe Bend rafting trips.</p>
<h3>Where to go</h3>
<p>Lee’s Ferry Boat Launch, Lees Ferry Road, Marble Canyon, AZ 86036. It is off Highway 89A near Navajo Bridge, about 45 to 50 minutes from Page. Follow Lee’s Ferry Road all the way to the boat ramp.</p>
<p><strong>Local tip:</strong> book your backhaul in advance, bring plenty of water and sun protection, and wear a life jacket. The Colorado River is cold year-round. While you’re in the area, don’t miss <a href="/waterholes-canyon-by-kayak-from-lees-ferry/">Waterholes Canyon</a> and the <a href="/glen-canyon-dam-overlook-page-arizona/">Glen Canyon Dam Overlook</a>.</p>''','DeX-Mw6JBku')

post('glen-canyon-dam-overlook-page-arizona','Glen Canyon Dam Overlook: A Quick, Spectacular Stop in Page','Oct 11, 2026','2026-10-11','Day Trips, Page',
 'img-2895','A short sandstone-step walk to a river view of Glen Canyon Dam. Address, trail length and photo tips for the overlook in Page, Arizona.',
 '''<p>A short walk down sandstone steps brings you to views of the Colorado River winding between red rock cliffs, with the 710-foot Glen Canyon Dam rising in the distance. It is a quick, scenic stop with excellent photo opportunities and a good look at one of the Southwest’s great engineering feats.</p>
<ul><li><strong>Address:</strong> Overlook Drive, Page, AZ 86040</li><li><strong>Trail:</strong> about 0.2 miles round trip, with uneven sandstone steps</li><li><strong>Tip:</strong> bring a camera and wear shoes with good traction</li></ul>
<p>It is a natural add-on if you’re visiting Page, Lake Powell or nearby Horseshoe Bend. See also our guide to <a href="/kayak-horseshoe-bend-from-lees-ferry/">kayaking Horseshoe Bend from Lee’s Ferry</a>.</p>''','DeV6gO5A6RU')

post('best-places-to-see-fall-leaves-in-flagstaff','Where to See Fall Leaves in Flagstaff: Our Favorite Spots','Oct 9, 2026','2026-10-09','Flagstaff, Fall',
 'img-7486','Five places to see fall color around Flagstaff, from downtown streets to Snowbowl Road and Schultz Pass, with crowd and driving tips.',
 '''<p>As a photographer and the wife of a local guide, our team has plenty of favorite places to see fall leaves in Flagstaff. Here are the ones we send people to.</p>
<h3>Downtown Flagstaff</h3>
<p>Tree-lined streets, quaint buildings, shops, galleries and great coffee make a picture-book setting.</p>
<h3>NAU campus</h3>
<p>Park near Macy’s coffee shop and walk a 2-mile loop through campus. It feels more like an East Coast town and is ideal for walking.</p>
<h3>Forest Service Roads 151 and 418 (Hart Prairie Road)</h3>
<p>A dirt road that circles the base of the mountain, and it is stunning. It is best in an AWD vehicle.</p>
<h3>Aspen Corner and Snowbowl Road</h3>
<p>This is where everyone goes. Expect heavy traffic and long waits for parking. It is worth it, but it is probably the most packed place in Arizona this week of the year. You can also ride the ski lifts through the leaves to the top of the mountain.</p>
<h3>Schultz Pass</h3>
<p>Takes you to the east side of the mountain. It is much quieter, and trails like the Sunset Trail make for a more relaxing day among the trees than Aspen Corner.</p>
<p>For more to do once the leaves have turned, see <a href="/flagstaff-arizonas-best-day-hikes/">Flagstaff’s best day hikes</a>.</p>''','DeTJqBfgRu_')

post('where-locals-love-to-eat-in-flagstaff-sosta-and-macys','Where Locals Love to Eat in Flagstaff: Sosta and Macy’s European Coffee House','Oct 1, 2026','2026-10-01','Flagstaff, Food',
 'chatgpt-image-apr-6-2026-09-44-31-am','Two Flagstaff favorites from our guides’ “Places Locals Love to Eat” series: Sosta downtown and the long-running, vegetarian Macy’s.',
 '''<p>Our “Places Locals Love to Eat in Flagstaff” series starts with two very different spots. For more, see our <a href="/best-places-to-eat-in-flagstaff-arizona/">Flagstaff food tour guide</a>.</p>
<h3>Sosta, 413 N San Francisco St</h3>
<p>One of Flagstaff’s newest places. Locals love it for the atmosphere and the plentiful seating, indoors and out. It is where people meet to talk about work, have a date without screens, or bring a book. The food is very good, and the prices reflect typical downtown Flagstaff. If you want something more hole-in-the-wall with good, cheap eats, we have those coming in the series too.</p>
<h3>Macy’s European Coffee House, 14 S. Beaver St</h3>
<p>Macy’s opened in 1980 on the south side of the tracks, long before the area was trendy, so it is a local landmark. It is a gathering spot built on nostalgia and solid food perfected over 45 years: cozy, quirky and vegetarian. The quiche and French cinnamon rolls are favorites, and a Bohemian (chocolate and cinnamon), a green chile burrito and coffee came to only $12.</p>
<p>Coffee is the heart of the place. Macy’s has done espresso since long before there was a Starbucks on every corner and roasts its own beans in Flagstaff. Come on a Tuesday and you can watch the big red roaster at work.</p>
<p>Both are local approved, and we love sending our guests their way.</p>''','Dd9f0GcgNS0',
 '<p><strong>Visiting Flagstaff?</strong> We run <a href="/book-your-tour/">Grand Canyon tours</a> and can point you to our favorite places to eat. <a href="/contact-us/">Get in touch</a>.</p>')

post('why-book-a-grand-canyon-sunset-tour','Why a Sunset Tour Is the Best Way to See the Grand Canyon','Sep 28, 2026','2026-09-28','Grand Canyon',
 'img-2455','Many visitors find the Grand Canyon underwhelming at midday. Golden hour is why the photos look the way they do. Here is why we recommend a sunset tour.',
 '''<p>People often see photos of the Grand Canyon and feel it doesn’t quite measure up when they arrive. The photographs that inspired your visit were very likely taken at golden hour, the two hours before sunset.</p>
<p>That is why we strongly recommend a sunset tour. It is worth moving the rest of your trip around to make sure you see the last rays of light hit the rim. You can’t fully appreciate this place until you watch the shadows lengthen.</p>
<p>If you want to see the canyon at its best, a sunset tour gives you much better odds.</p>''','Dd2dKNXgWMJ',
 '<p><a class="btn" href="/grand-canyon-sunset-star-gazing-tour/">See the sunset &amp; star gazing tour</a></p>')

post('private-grand-canyon-tour-east-rim-volcanoes-and-wupatki','A Private Tour Done Your Way: Volcanoes, Ruins and the Grand Canyon’s East Rim','Sep 28, 2026','2026-09-28','Private Tours, Grand Canyon',
 'img-2384','One of the biggest perks of a private tour is rewriting the itinerary. A recent day: Sunset Crater, Wupatki, Cameron Trading Post and the East Rim.',
 '''<p>What is the advantage of a private tour for your Grand Canyon visit? You can rewrite the itinerary to fit your pace and interests.</p>
<p>A recent guest had already seen the South Rim and wanted to explore the volcanic craters east of Flagstaff on her way to the East Rim instead. Here is how that day went:</p>
<ol><li>Sunset Crater park, to see its flora and fauna.</li><li>Down the hill to Wupatki National Monument, to look at the Native American ruins.</li><li>Toward the Painted Desert, with a side trip to Cameron Trading Post and its huge rug and pottery showroom.</li><li>Desert View Watchtower and the East Rim Drive of the Grand Canyon.</li></ol>
<p>If you’d like a private tour of the area for a group of 1 to 11 people, we’d love to tailor a day to your needs. Picnic lunches from Eat n’ Run Flagstaff are also available.</p>''','Dd0gPX9gLD5',
 '<p><a class="btn" href="/private-guided-tours-from-flagstaff-williams-grand-canyon/">Explore private tours</a></p>')

def card(p,n=''):
    m=man[p['img']]; fs=sorted(m['files']); ss=', '.join(f'/img/{f} {w}w' for w,f in fs)
    return (f'<article class="post-card"><a href="/{p["slug"]}/"><img src="/img/{fs[-1][1]}" srcset="{ss}" sizes="(min-width:62rem) 30vw, (min-width:36rem) 45vw, 92vw" width="{m["w"]}" height="{m["h"]}" alt="{html.escape(p["title"])}" loading="lazy" decoding="async">'
            f'<p class="meta">{p["date"]} · {p["cats"]}</p><h2>{p["title"]}</h2><p>{p["desc"]}</p></a></article>')

for p in P:
    m=man[p['img']]; fs=sorted(m['files']); ss=', '.join(f'/img/{f} {w}w' for w,f in fs)
    meta={"kind":"post","title":p['title']+" - TrekWest Arizona Adventure Tours","desc":"","og":"","h1":p['title'],"og_img":p['img']}
    fig=f'<figure><img src="/img/{fs[-1][1]}" srcset="{ss}" sizes="(min-width:900px) 40vw, 92vw" width="{m["w"]}" height="{m["h"]}" alt="" loading="lazy" decoding="async"></figure>'
    out=(f'<!--meta {json.dumps(meta,ensure_ascii=False)} -->\n<section class="band">\n<div class="row">\n<div class="col">\n@@H1@@\n'
         f'<p>by info@trekwest.net | {p["date"]} | {p["cats"]} | <a href="/{p["slug"]}/#respond">0 comments</a></p>\n{fig}\n</div>\n</div>\n</section>\n'
         f'<section class="band">\n<div class="row">\n<div class="col">\n{p["body"]}\n{p["cta"]}\n{src(p["ig"],p["date"])}\n</div>\n</div>\n</section>\n')
    open(f'src/pages/{p["slug"]}.html','w').write(out)
    site['pages'][f'/{p["slug"]}/']={'priority':0.5,'og':p['img'],'desc':p['desc'],'date':p['iso']}

# indexes: prepend cards (newest first), skip if already added
cards=''.join(card(p) for p in P)
for f in ['grand-canyon-blog','trail-mix-trekwest-tours-northern-arizona-blog-newsletter']:
    path=f'src/pages/{f}.html'; c=open(path).read()
    if P[0]['slug'] not in c:
        c=re.sub(r'(<div class="posts"[^>]*>)',lambda m:m.group(1)+cards,c,count=1)
        if 'class="recent"' in c:
            li=''.join(f'<li><a href="/{p["slug"]}/">{p["title"]}</a></li>' for p in P[:5])
            c=c.replace('<ul class="recent">','<ul class="recent">'+li,1)
        open(path,'w').write(c)
json.dump(site,open('src/site.json','w'),indent=2,ensure_ascii=False)
print(len(P),'posts')
