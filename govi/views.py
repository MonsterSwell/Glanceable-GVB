from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404
from django.shortcuts import render_to_response

import logging
import urllib2
import datetime
import time
import json

from xml.dom.minidom import parseString

logger = logging.getLogger(__name__)

HALTES = [
     {
       "lat": "4.89891084495292", 
       "lon": "52.5963476762811", 
       "name": "schermerhorn, Schermerhorn, v.d.Hulst", 
       "id": "36370530"
     }, 
     {
       "lat": "4.84443544756503", 
       "lon": "52.5544100720921", 
       "name": "de rijp, De Rijp, Julianalaan", 
       "id": "36380010"
     }, 
     {
       "lat": "4.84437293255423", 
       "lon": "52.5546973826828", 
       "name": "de rijp, De Rijp, Julianalaan", 
       "id": "36380520"
     }, 
     {
       "lat": "4.84349129605905", 
       "lon": "52.5568413339838", 
       "name": "de rijp, De Rijp, Fluytschip", 
       "id": "36380540"
     }, 
     {
       "lat": "4.84336712241695", 
       "lon": "52.5561487369336", 
       "name": "de rijp, De Rijp, Fluytschip", 
       "id": "36380630"
     }, 
     {
       "lat": "4.90768515221814", 
       "lon": "52.540041907501", 
       "name": "middenbeemster, Middenbeemster, De Knip", 
       "id": "36470040"
     }, 
     {
       "lat": "4.91246633133887", 
       "lon": "52.5477632944538", 
       "name": "middenbeemster, Middenbeemster, De Buurt", 
       "id": "36470080"
     }, 
     {
       "lat": "4.91077207717074", 
       "lon": "52.5449254895472", 
       "name": "middenbeemster, Middenbeemster, K.Hogetoornlaan", 
       "id": "36470150"
     }, 
     {
       "lat": "4.9080532482022", 
       "lon": "52.5400793431272", 
       "name": "middenbeemster, Middenbeemster, De Knip", 
       "id": "36470170"
     }, 
     {
       "lat": "4.91307777216347", 
       "lon": "52.5484847260353", 
       "name": "middenbeemster, Middenbeemster, De Buurt", 
       "id": "36470200"
     }, 
     {
       "lat": "4.91428028805593", 
       "lon": "52.5504577518905", 
       "name": "middenbeemster, Middenbeemster, C.ten Hoopestraat", 
       "id": "36470520"
     }, 
     {
       "lat": "4.91842420615232", 
       "lon": "52.557304563267", 
       "name": "middenbeemster, Middenbeemster, Tuyp", 
       "id": "36470540"
     }, 
     {
       "lat": "4.92502978058392", 
       "lon": "52.5686185269843", 
       "name": "middenbeemster, Middenbeemster, Velzeboer", 
       "id": "36470550"
     }, 
     {
       "lat": "4.92271376039423", 
       "lon": "52.564448366768", 
       "name": "middenbeemster, Middenbeemster, Hobrederweg", 
       "id": "36470560"
     }, 
     {
       "lat": "4.92197073139259", 
       "lon": "52.5635826760411", 
       "name": "middenbeemster, Middenbeemster, Hobrederweg", 
       "id": "36470570"
     }, 
     {
       "lat": "4.92532372587738", 
       "lon": "52.5687185307243", 
       "name": "middenbeemster, Middenbeemster, Velzeboer", 
       "id": "36470580"
     }, 
     {
       "lat": "4.91866666667579", 
       "lon": "52.5580784308156", 
       "name": "middenbeemster, Middenbeemster, Tuyp", 
       "id": "36470590"
     }, 
     {
       "lat": "4.92928294047645", 
       "lon": "52.5752137021335", 
       "name": "middenbeemster, Middenbeemster, Witte Kan", 
       "id": "36470600"
     }, 
     {
       "lat": "4.91410279462723", 
       "lon": "52.5505109689771", 
       "name": "middenbeemster, Middenbeemster, C.ten Hoopestraat", 
       "id": "36470610"
     }, 
     {
       "lat": "4.93768917536923", 
       "lon": "52.5146530964352", 
       "name": "zuidoostbeemster, Zuidoostbeemster, D.Dekkerstraat", 
       "id": "36570020"
     }, 
     {
       "lat": "4.93113329449539", 
       "lon": "52.5161110074366", 
       "name": "zuidoostbeemster, Zuidoostbeemster, Kolkpad", 
       "id": "36570040"
     }, 
     {
       "lat": "4.92414165138335", 
       "lon": "52.5183397749355", 
       "name": "zuidoostbeemster, Zuidoostbeemster, Zuiderweg", 
       "id": "36570060"
     }, 
     {
       "lat": "4.93151863139424", 
       "lon": "52.5158878022713", 
       "name": "zuidoostbeemster, Zuidoostbeemster, Kolkpad", 
       "id": "36570110"
     }, 
     {
       "lat": "4.90365013508517", 
       "lon": "52.5329704437466", 
       "name": "zuidoostbeemster, Zuidoostbeemster, Volgerweg", 
       "id": "36570120"
     }, 
     {
       "lat": "4.90421869806502", 
       "lon": "52.5321908550542", 
       "name": "zuidoostbeemster, Zuidoostbeemster, Volgerweg", 
       "id": "36570510"
     }, 
     {
       "lat": "4.91165000787998", 
       "lon": "52.5304862906277", 
       "name": "zuidoostbeemster, Zuidoostbeemster, Arbeid Adelt", 
       "id": "36570530"
     }, 
     {
       "lat": "4.92643024699127", 
       "lon": "52.5220964304614", 
       "name": "zuidoostbeemster, Zuidoostbeemster, Nekkerweg", 
       "id": "36570540"
     }, 
     {
       "lat": "4.92250765920423", 
       "lon": "52.5280128211916", 
       "name": "zuidoostbeemster, Zuidoostbeemster, Jonk", 
       "id": "36570550"
     }, 
     {
       "lat": "4.92842974717612", 
       "lon": "52.5267686347039", 
       "name": "zuidoostbeemster, Zuidoostbeemster, Halfweg", 
       "id": "36570560"
     }, 
     {
       "lat": "4.92851937111042", 
       "lon": "52.52665214496", 
       "name": "zuidoostbeemster, Zuidoostbeemster, Halfweg", 
       "id": "36570570"
     }, 
     {
       "lat": "4.92173847856447", 
       "lon": "52.5282884167437", 
       "name": "zuidoostbeemster, Zuidoostbeemster, Jonk", 
       "id": "36570580"
     }, 
     {
       "lat": "4.92623927448197", 
       "lon": "52.5220417645268", 
       "name": "zuidoostbeemster, Zuidoostbeemster, Nekkerweg", 
       "id": "36570590"
     }, 
     {
       "lat": "4.91153076221583", 
       "lon": "52.5306116363749", 
       "name": "zuidoostbeemster, Zuidoostbeemster, Arbeid Adelt", 
       "id": "36570600"
     }, 
     {
       "lat": "4.94452412108965", 
       "lon": "52.5073540442835", 
       "name": "purmerend, Purmerend, Tramplein", 
       "id": "37400100"
     }, 
     {
       "lat": "4.94417027421837", 
       "lon": "52.507388673445", 
       "name": "purmerend, Purmerend, Tramplein", 
       "id": "37400103"
     }, 
     {
       "lat": "4.94579662724303", 
       "lon": "52.5111964119202", 
       "name": "purmerend, Purmerend, Ged.Singelgracht", 
       "id": "37400110"
     }, 
     {
       "lat": "4.94550661221656", 
       "lon": "52.5107369747119", 
       "name": "purmerend, Purmerend, Ged.Singelgracht", 
       "id": "37400160"
     }, 
     {
       "lat": "4.93873881911479", 
       "lon": "52.514288583566", 
       "name": "zuidoostbeemster, Zuidoostbeemster, D.Dekkerstraat", 
       "id": "37403510"
     }, 
     {
       "lat": "4.94183955872605", 
       "lon": "52.5135812672025", 
       "name": "zuidoostbeemster, Zuidoostbeemster, W.Sluislaan", 
       "id": "37403530"
     }, 
     {
       "lat": "5.05639288707867", 
       "lon": "52.6586049365412", 
       "name": "hoorn, Hoorn, Beurtschip", 
       "id": "38000070"
     }, 
     {
       "lat": "5.05821042423158", 
       "lon": "52.656677759948", 
       "name": "hoorn, Hoorn, Blokmergouw", 
       "id": "38000090"
     }, 
     {
       "lat": "5.06675455775853", 
       "lon": "52.6503382427186", 
       "name": "hoorn, Hoorn, Wabenstraat", 
       "id": "38000130"
     }, 
     {
       "lat": "5.067003863973", 
       "lon": "52.6505995389345", 
       "name": "hoorn, Hoorn, Wabenstraat", 
       "id": "38000200"
     }, 
     {
       "lat": "5.05419227058151", 
       "lon": "52.6447317512802", 
       "name": "hoorn, Hoorn, Station NS", 
       "id": "38000235"
     }, 
     {
       "lat": "5.05601399732682", 
       "lon": "52.6598530824557", 
       "name": "hoorn, Hoorn, Beurtschip", 
       "id": "38000260"
     }, 
     {
       "lat": "5.04612595866442", 
       "lon": "52.6427137607926", 
       "name": "hoorn, Hoorn, Zuiderkruisstraat", 
       "id": "38000510"
     }, 
     {
       "lat": "5.03926860638578", 
       "lon": "52.641103182763", 
       "name": "hoorn, Hoorn, Astronautenweg", 
       "id": "38000530"
     }, 
     {
       "lat": "5.0361653768481", 
       "lon": "52.6393415795021", 
       "name": "hoorn, Hoorn, Poolster", 
       "id": "38000540"
     }, 
     {
       "lat": "5.03610456471169", 
       "lon": "52.6395570904496", 
       "name": "hoorn, Hoorn, Poolster", 
       "id": "38000550"
     }, 
     {
       "lat": "5.04034650512854", 
       "lon": "52.6411782279207", 
       "name": "hoorn, Hoorn, Astronautenweg", 
       "id": "38000560"
     }, 
     {
       "lat": "5.04679092980589", 
       "lon": "52.642697691641", 
       "name": "hoorn, Hoorn, Zuiderkruisstraat", 
       "id": "38000580"
     }, 
     {
       "lat": "5.04586105821395", 
       "lon": "52.6501992408925", 
       "name": "Hoorn, Hoorn, Keern", 
       "id": "38001010"
     }, 
     {
       "lat": "5.06706395237494", 
       "lon": "52.6443716596568", 
       "name": "hoorn, Hoorn, J.D.Pollstraat", 
       "id": "38001020"
     }, 
     {
       "lat": "5.03991836277106", 
       "lon": "52.6654780164141", 
       "name": "Hoorn, Hoorn, Stijgbeugel", 
       "id": "38001030"
     }, 
     {
       "lat": "5.04100188634129", 
       "lon": "52.6630366976129", 
       "name": "Hoorn, Hoorn, Hoefijzer", 
       "id": "38001050"
     }, 
     {
       "lat": "5.0412091719882", 
       "lon": "52.6629923653444", 
       "name": "Hoorn, Hoorn, Hoefijzer", 
       "id": "38001120"
     }, 
     {
       "lat": "5.06759335890849", 
       "lon": "52.6447145923181", 
       "name": "hoorn, Hoorn, J.D.Pollstraat", 
       "id": "38001130"
     }, 
     {
       "lat": "5.03994530066597", 
       "lon": "52.6658106156282", 
       "name": "Hoorn, Hoorn, Stijgbeugel", 
       "id": "38001140"
     }, 
     {
       "lat": "5.0646354101626", 
       "lon": "52.6551945156009", 
       "name": "hoorn, Hoorn, Nieuwe Steen", 
       "id": "38003020"
     }, 
     {
       "lat": "5.06788441079268", 
       "lon": "52.6555088403495", 
       "name": "hoorn, Hoorn, Copernicus", 
       "id": "38003030"
     }, 
     {
       "lat": "5.06820933948522", 
       "lon": "52.6555366731908", 
       "name": "hoorn, Hoorn, Copernicus", 
       "id": "38003040"
     }, 
     {
       "lat": "5.06522785606879", 
       "lon": "52.6550163793503", 
       "name": "hoorn, Hoorn, Nieuwe Steen", 
       "id": "38003050"
     }, 
     {
       "lat": "5.04393061716035", 
       "lon": "52.6684553822398", 
       "name": "Hoorn, Hoorn, Sportpark", 
       "id": "38004010"
     }, 
     {
       "lat": "5.0474544288048", 
       "lon": "52.6505273370557", 
       "name": "hoorn, Hoorn, Geldelozeweg", 
       "id": "38004020"
     }, 
     {
       "lat": "5.04664556543622", 
       "lon": "52.665299746378", 
       "name": "hoorn, Hoorn, Wogmergouw", 
       "id": "38004030"
     }, 
     {
       "lat": "5.04604830483001", 
       "lon": "52.6660709208683", 
       "name": "hoorn, Hoorn, Wogmergouw", 
       "id": "38004120"
     }, 
     {
       "lat": "5.08518568132597", 
       "lon": "52.6583220287455", 
       "name": "hoorn, Hoorn, Maasweg", 
       "id": "38110100"
     }, 
     {
       "lat": "5.08509725216788", 
       "lon": "52.6582858560754", 
       "name": "hoorn, Hoorn, Maasweg", 
       "id": "38110130"
     }, 
     {
       "lat": "5.07732317544546", 
       "lon": "52.6561898544253", 
       "name": "hoorn, Hoorn, IJsselweg", 
       "id": "38110230"
     }, 
     {
       "lat": "5.07745738512901", 
       "lon": "52.6560194499813", 
       "name": "hoorn, Hoorn, IJsselweg", 
       "id": "38110240"
     }, 
     {
       "lat": "5.07175449862306", 
       "lon": "52.6578378237903", 
       "name": "hoorn, Hoorn, Oscar Romero", 
       "id": "38110650"
     }, 
     {
       "lat": "5.09625901441857", 
       "lon": "52.6466305082908", 
       "name": "hoorn, Hoorn, Scheldeweg", 
       "id": "38113010"
     }, 
     {
       "lat": "5.08824292809362", 
       "lon": "52.6542855798637", 
       "name": "Hoorn, Hoorn, Luifel", 
       "id": "38113020"
     }, 
     {
       "lat": "5.08921918803737", 
       "lon": "52.6541532233442", 
       "name": "Hoorn, Hoorn, Luifel", 
       "id": "38113070"
     }, 
     {
       "lat": "4.48002143322605", 
       "lon": "52.1703718962602", 
       "name": "leiden, Leiden, Posthof", 
       "id": "54440030"
     }, 
     {
       "lat": "4.48001229958985", 
       "lon": "52.1701021742142", 
       "name": "leiden, Leiden, Posthof", 
       "id": "54440640"
     }, 
     {
       "lat": "4.48109930257347", 
       "lon": "52.1669645874712", 
       "name": "leiden, Leiden, CS Noordzijde/LUMC", 
       "id": "54440870"
     }, 
     {
       "lat": "4.47990928278265", 
       "lon": "52.1665419768458", 
       "name": "leiden, Leiden, CS Noordzijde/LUMC", 
       "id": "54440880"
     }, 
     {
       "lat": "4.47039333395352", 
       "lon": "52.1750883022662", 
       "name": "oegstgeest, Oegstgeest, Hendrik Kraemerpark", 
       "id": "54443010"
     }, 
     {
       "lat": "4.47402936955392", 
       "lon": "52.1731570238819", 
       "name": "leiden, Leiden, Lijsterstraat", 
       "id": "54443030"
     }, 
     {
       "lat": "4.47383493284594", 
       "lon": "52.1733712406358", 
       "name": "leiden, Leiden, Lijsterstraat", 
       "id": "54443120"
     }, 
     {
       "lat": "4.48865871079044", 
       "lon": "52.1864462726304", 
       "name": "oegstgeest, Oegstgeest, Pres. Kennedylaan", 
       "id": "54540010"
     }, 
     {
       "lat": "4.46506784807412", 
       "lon": "52.1802241272194", 
       "name": "oegstgeest, Oegstgeest, Leidsebuurt", 
       "id": "54550090"
     }, 
     {
       "lat": "4.46675370244411", 
       "lon": "52.187805509498", 
       "name": "oegstgeest, Oegstgeest, Wijttenbachweg", 
       "id": "54550100"
     }, 
     {
       "lat": "4.46620789804852", 
       "lon": "52.1844935264287", 
       "name": "oegstgeest, Oegstgeest, Duinzichtstraat", 
       "id": "54550110"
     }, 
     {
       "lat": "4.46600492509419", 
       "lon": "52.1837009642746", 
       "name": "oegstgeest, Oegstgeest, Duinzichtstraat", 
       "id": "54550120"
     }, 
     {
       "lat": "4.47112845825817", 
       "lon": "52.1748872779031", 
       "name": "oegstgeest, Oegstgeest, Hendrik Kraemerpark", 
       "id": "54550520"
     }, 
     {
       "lat": "4.46702360549118", 
       "lon": "52.1775608502549", 
       "name": "oegstgeest, Oegstgeest, De Kempenaerstraat", 
       "id": "54550540"
     }, 
     {
       "lat": "4.46519836442279", 
       "lon": "52.1795689940417", 
       "name": "oegstgeest, Oegstgeest, Leidsebuurt", 
       "id": "54550560"
     }, 
     {
       "lat": "4.46761982848254", 
       "lon": "52.1770082169388", 
       "name": "oegstgeest, Oegstgeest, De Kempenaerstraat", 
       "id": "54550650"
     }, 
     {
       "lat": "4.46722652538431", 
       "lon": "52.1896967553709", 
       "name": "oegstgeest, Oegstgeest, Dorpsstraat", 
       "id": "54554010"
     }, 
     {
       "lat": "4.46741272290924", 
       "lon": "52.1898869623533", 
       "name": "oegstgeest, Oegstgeest, Dorpsstraat", 
       "id": "54554040"
     }, 
     {
       "lat": "4.48506709975855", 
       "lon": "52.1876053402513", 
       "name": "oegstgeest, Oegstgeest, Pres. Kennedylaan", 
       "id": "54559030"
     }, 
     {
       "lat": "4.47520483422225", 
       "lon": "52.1900283185461", 
       "name": "oegstgeest, Oegstgeest, Narcissenlaan", 
       "id": "54559040"
     }, 
     {
       "lat": "4.47517430242682", 
       "lon": "52.1900910012286", 
       "name": "oegstgeest, Oegstgeest, Narcissenlaan", 
       "id": "54559050"
     }, 
     {
       "lat": "4.46570507842621", 
       "lon": "52.2293414807419", 
       "name": "noordwijk, Noordwijk, Noordwijkerhoek", 
       "id": "54650030"
     }, 
     {
       "lat": "4.46590588365995", 
       "lon": "52.2295407901836", 
       "name": "noordwijk, Noordwijk, Noordwijkerhoek", 
       "id": "54650060"
     }, 
     {
       "lat": "4.4912348229723", 
       "lon": "52.2212596798216", 
       "name": "voorhout, Voorhout, Oosthoutlaan", 
       "id": "54650420"
     }, 
     {
       "lat": "4.49060993503802", 
       "lon": "52.2217672706153", 
       "name": "voorhout, Voorhout, Oosthoutlaan", 
       "id": "54650430"
     }, 
     {
       "lat": "4.48536930966394", 
       "lon": "52.2232733569579", 
       "name": "voorhout, Voorhout, Gemeentehuis/Station", 
       "id": "54650500"
     }, 
     {
       "lat": "4.48192344601931", 
       "lon": "52.2214313551861", 
       "name": "voorhout, Voorhout, RK Kerk", 
       "id": "54650540"
     }, 
     {
       "lat": "4.48154390604528", 
       "lon": "52.2213835036654", 
       "name": "voorhout, Voorhout, RK Kerk", 
       "id": "54650590"
     }, 
     {
       "lat": "4.48560989268776", 
       "lon": "52.2236796675208", 
       "name": "voorhout, Voorhout, Gemeentehuis/Station", 
       "id": "54650610"
     }, 
     {
       "lat": "4.4349163551051", 
       "lon": "52.2480806228937", 
       "name": "noordwijk, Noordwijk, Vuurtorenplein", 
       "id": "54660050"
     }, 
     {
       "lat": "4.44153488343329", 
       "lon": "52.2301840937529", 
       "name": "noordwijk, Noordwijk, Boekerslootlaan", 
       "id": "54660060"
     }, 
     {
       "lat": "4.43989219822282", 
       "lon": "52.2447859585605", 
       "name": "noordwijk, Noordwijk, Piet Heinplein", 
       "id": "54660070"
     }, 
     {
       "lat": "4.4509522751319", 
       "lon": "52.2396878698213", 
       "name": "noordwijk, Noordwijk, van de Mortelstraat", 
       "id": "54660110"
     }, 
     {
       "lat": "4.44969644014229", 
       "lon": "52.24022619738", 
       "name": "noordwijk, Noordwijk, van de Mortelstraat", 
       "id": "54660160"
     }, 
     {
       "lat": "4.43979804427794", 
       "lon": "52.2450818181177", 
       "name": "noordwijk, Noordwijk, Piet Heinplein", 
       "id": "54660200"
     }, 
     {
       "lat": "4.4423317333053", 
       "lon": "52.2291927650192", 
       "name": "noordwijk, Noordwijk, Boekerslootlaan", 
       "id": "54660210"
     }, 
     {
       "lat": "4.43426634116795", 
       "lon": "52.2476619190568", 
       "name": "noordwijk, Noordwijk, Vuurtorenplein", 
       "id": "54660220"
     }, 
     {
       "lat": "4.63938908601711", 
       "lon": "52.3873825828047", 
       "name": "haarlem, Haarlem, Station NS ingang", 
       "id": "55000030"
     }, 
     {
       "lat": "4.63753717563184", 
       "lon": "52.3874427763913", 
       "name": "haarlem, Haarlem, Station NS", 
       "id": "55000053"
     }, 
     {
       "lat": "4.6382182931005", 
       "lon": "52.3871235229837", 
       "name": "haarlem, Haarlem, Station NS", 
       "id": "55000054"
     }, 
     {
       "lat": "4.62977022776623", 
       "lon": "52.3725992797917", 
       "name": "haarlem, Haarlem, Dreef", 
       "id": "55000100"
     }, 
     {
       "lat": "4.6295811892827", 
       "lon": "52.3724902153282", 
       "name": "haarlem, Haarlem, Dreef", 
       "id": "55000170"
     }, 
     {
       "lat": "4.6376107679505", 
       "lon": "52.3874342543861", 
       "name": "haarlem, Haarlem, Station NS", 
       "id": "55000253"
     }, 
     {
       "lat": "4.64562953464723", 
       "lon": "52.3699763500443", 
       "name": "haarlem, Haarlem, Schipholweg/Europaweg", 
       "id": "55001070"
     }, 
     {
       "lat": "4.64562953464723", 
       "lon": "52.3699763500443", 
       "name": "haarlem, Haarlem, Schipholweg/Europaweg", 
       "id": "55001075"
     }, 
     {
       "lat": "4.64453513323816", 
       "lon": "52.3695650341486", 
       "name": "haarlem, Haarlem, Europaweg/Schipholweg", 
       "id": "55001240"
     }, 
     {
       "lat": "4.64497885110999", 
       "lon": "52.3702508971361", 
       "name": "haarlem, Haarlem, Schipholweg/Europaweg", 
       "id": "55001241"
     }, 
     {
       "lat": "4.64497870072039", 
       "lon": "52.3702598840902", 
       "name": "haarlem, Haarlem, Schipholweg/Europaweg", 
       "id": "55001245"
     }, 
     {
       "lat": "4.63262506242711", 
       "lon": "52.380014549294", 
       "name": "haarlem, Haarlem, Centrum/Verwulft", 
       "id": "55002090"
     }, 
     {
       "lat": "4.62936807745548", 
       "lon": "52.3755087871446", 
       "name": "haarlem, Haarlem, Tempeliersstraat", 
       "id": "55002110"
     }, 
     {
       "lat": "4.62916203926508", 
       "lon": "52.3755344318373", 
       "name": "haarlem, Haarlem, Tempeliersstraat", 
       "id": "55002111"
     }, 
     {
       "lat": "4.62992791470847", 
       "lon": "52.3754045144788", 
       "name": "haarlem, Haarlem, Tempeliersstraat", 
       "id": "55002112"
     }, 
     {
       "lat": "4.63040133219304", 
       "lon": "52.3752008198827", 
       "name": "haarlem, Haarlem, Tempeliersstraat", 
       "id": "55002240"
     }, 
     {
       "lat": "4.62963546164268", 
       "lon": "52.375330740319", 
       "name": "haarlem, Haarlem, Tempeliersstraat", 
       "id": "55002242"
     }, 
     {
       "lat": "4.62953175212403", 
       "lon": "52.3753840040796", 
       "name": "haarlem, Haarlem, Tempeliersstraat", 
       "id": "55002243"
     }, 
     {
       "lat": "4.63276993060377", 
       "lon": "52.3801323150116", 
       "name": "haarlem, Haarlem, Centrum/Verwulft", 
       "id": "55002260"
     }, 
     {
       "lat": "4.65584799350893", 
       "lon": "52.370066881761", 
       "name": "haarlem, Haarlem, Burg. Reinaldapark", 
       "id": "55002350"
     }, 
     {
       "lat": "4.62844182124524", 
       "lon": "52.3815786728341", 
       "name": "haarlem, Haarlem, Raaksbrug", 
       "id": "55005520"
     }, 
     {
       "lat": "4.62673621132113", 
       "lon": "52.3782601851415", 
       "name": "haarlem, Haarlem, Stadsschouwburg", 
       "id": "55005540"
     }, 
     {
       "lat": "4.62691258541112", 
       "lon": "52.378252329939", 
       "name": "haarlem, Haarlem, Stadsschouwburg", 
       "id": "55005550"
     }, 
     {
       "lat": "4.62829119547843", 
       "lon": "52.3809395671836", 
       "name": "haarlem, Haarlem, Raaksbrug", 
       "id": "55005570"
     }, 
     {
       "lat": "4.63727696533972", 
       "lon": "52.3724313588316", 
       "name": "haarlem, Haarlem, Rustenburgerlaan", 
       "id": "55007510"
     }, 
     {
       "lat": "4.65308324760987", 
       "lon": "52.3703194063146", 
       "name": "haarlem, Haarlem, Burg. Reinaldapark", 
       "id": "55007540"
     }, 
     {
       "lat": "4.63644893107224", 
       "lon": "52.3727676510424", 
       "name": "haarlem, Haarlem, Rustenburgerlaan", 
       "id": "55007580"
     }, 
     {
       "lat": "4.62544647747915", 
       "lon": "52.3610040841963", 
       "name": "heemstede, Heemstede, Blauwe Brug", 
       "id": "55008510"
     }, 
     {
       "lat": "4.62735645404607", 
       "lon": "52.3652047338813", 
       "name": "haarlem, Haarlem, Spanjaardslaan", 
       "id": "55008530"
     }, 
     {
       "lat": "4.6263995516616", 
       "lon": "52.3644975296595", 
       "name": "haarlem, Haarlem, Spanjaardslaan", 
       "id": "55008600"
     }, 
     {
       "lat": "4.67161863667345", 
       "lon": "52.3500303796216", 
       "name": "ONBEKEND, dummyfinancierwissel ZTG", 
       "id": "55049980"
     }, 
     {
       "lat": "4.71953957242753", 
       "lon": "52.3861269565385", 
       "name": "halfweg, Halfweg, Vinkebrug", 
       "id": "55130020"
     }, 
     {
       "lat": "4.62468327464969", 
       "lon": "52.3558670583498", 
       "name": "heemstede, Heemstede, Lanckhorstlaan", 
       "id": "55140090"
     }, 
     {
       "lat": "4.62412278817379", 
       "lon": "52.3474866774728", 
       "name": "heemstede, Heemstede, Wipperplein", 
       "id": "55140100"
     }, 
     {
       "lat": "4.62453864028877", 
       "lon": "52.350617166005", 
       "name": "heemstede, Heemstede, Zandvaartkade", 
       "id": "55140120"
     }, 
     {
       "lat": "4.62425871434164", 
       "lon": "52.3523859877725", 
       "name": "heemstede, Heemstede, Julianaplein", 
       "id": "55140130"
     }, 
     {
       "lat": "4.62482198587866", 
       "lon": "52.3529199064", 
       "name": "heemstede, Heemstede, Julianaplein", 
       "id": "55140140"
     }, 
     {
       "lat": "4.62383236430696", 
       "lon": "52.3490127568691", 
       "name": "heemstede, Heemstede, Zandvaartkade", 
       "id": "55140150"
     }, 
     {
       "lat": "4.62529604737034", 
       "lon": "52.3569405693761", 
       "name": "heemstede, Heemstede, Lanckhorstlaan", 
       "id": "55140160"
     }, 
     {
       "lat": "4.62357459194279", 
       "lon": "52.346081019863", 
       "name": "heemstede, Heemstede, Wipperplein", 
       "id": "55140230"
     }, 
     {
       "lat": "4.637426194351", 
       "lon": "52.3375411554364", 
       "name": "cruquius, Cruquius, Ringvaartbrug", 
       "id": "55142020"
     }, 
     {
       "lat": "4.63079691231793", 
       "lon": "52.3433950658223", 
       "name": "heemstede, Heemstede, Cruquiusweg", 
       "id": "55142280"
     }, 
     {
       "lat": "4.63198806826433", 
       "lon": "52.3423870346241", 
       "name": "heemstede, Heemstede, Cruquiusweg", 
       "id": "55142290"
     }, 
     {
       "lat": "4.624941524784", 
       "lon": "52.3621962282481", 
       "name": "heemstede, Heemstede, Blauwe Brug", 
       "id": "55146020"
     }, 
     {
       "lat": "4.62501379466049", 
       "lon": "52.358844194803", 
       "name": "heemstede, Heemstede, Cesar Francklaan", 
       "id": "55146050"
     }, 
     {
       "lat": "4.72020390580231", 
       "lon": "52.3859060051502", 
       "name": "halfweg, Halfweg, Vinkebrug", 
       "id": "55230010"
     }, 
     {
       "lat": "4.75279643416215", 
       "lon": "52.384017907069", 
       "name": "halfweg, Halfweg, Oranje Nassaustraat", 
       "id": "55230040"
     }, 
     {
       "lat": "4.75604666250725", 
       "lon": "52.383729690605", 
       "name": "halfweg, Halfweg, Oranje Nassaustraat", 
       "id": "55230050"
     }, 
     {
       "lat": "4.74508612813223", 
       "lon": "52.3859716376704", 
       "name": "halfweg, Halfweg, Suikerfabriek", 
       "id": "55230060"
     }, 
     {
       "lat": "4.75434083879553", 
       "lon": "52.3828397836185", 
       "name": "halfweg, Halfweg, Oranje Nassaustraat", 
       "id": "55231210"
     }, 
     {
       "lat": "4.75118886887824", 
       "lon": "52.3793536094039", 
       "name": "zwanenburg, Zwanenburg, Wilgenlaan", 
       "id": "55232150"
     }, 
     {
       "lat": "4.72838287223076", 
       "lon": "52.3851069377599", 
       "name": "zwanenburg, Zwanenburg, Seevank", 
       "id": "55232180"
     }, 
     {
       "lat": "4.74440101152465", 
       "lon": "52.3744635414645", 
       "name": "zwanenburg, Zwanenburg, Piersonstraat", 
       "id": "55232200"
     }, 
     {
       "lat": "4.74518681153923", 
       "lon": "52.3739465122765", 
       "name": "zwanenburg, Zwanenburg, Piersonstraat", 
       "id": "55232210"
     }, 
     {
       "lat": "4.74710422710923", 
       "lon": "52.3764195521298", 
       "name": "zwanenburg, Zwanenburg, De Olm", 
       "id": "55232250"
     }, 
     {
       "lat": "4.74656621621975", 
       "lon": "52.376048142477", 
       "name": "zwanenburg, Zwanenburg, De Olm", 
       "id": "55232260"
     }, 
     {
       "lat": "4.7379187512854", 
       "lon": "52.377888477303", 
       "name": "zwanenburg, Zwanenburg, Troelstralaan", 
       "id": "55232290"
     }, 
     {
       "lat": "4.73858352710871", 
       "lon": "52.3776224866369", 
       "name": "zwanenburg, Zwanenburg, Troelstralaan", 
       "id": "55232300"
     }, 
     {
       "lat": "4.73575623508629", 
       "lon": "52.3791348920498", 
       "name": "zwanenburg, Zwanenburg, Nauerna", 
       "id": "55232310"
     }, 
     {
       "lat": "4.73528457929368", 
       "lon": "52.3792491376449", 
       "name": "zwanenburg, Zwanenburg, Nauerna", 
       "id": "55232320"
     }, 
     {
       "lat": "4.72866887665866", 
       "lon": "52.3846411630003", 
       "name": "zwanenburg, Zwanenburg, Seevank", 
       "id": "55232380"
     }, 
     {
       "lat": "4.73066790884269", 
       "lon": "52.383555751427", 
       "name": "zwanenburg, Zwanenburg, Kinheim", 
       "id": "55232400"
     }, 
     {
       "lat": "4.73094722830996", 
       "lon": "52.3835393241403", 
       "name": "zwanenburg, Zwanenburg, Kinheim", 
       "id": "55232401"
     }, 
     {
       "lat": "4.75122996140479", 
       "lon": "52.3795605493465", 
       "name": "zwanenburg, Zwanenburg, Wilgenlaan", 
       "id": "55232480"
     }, 
     {
       "lat": "4.60014285743153", 
       "lon": "52.3217497685818", 
       "name": "bennebroek, Bennebroek, Schoollaan", 
       "id": "55241010"
     }, 
     {
       "lat": "4.60058443611741", 
       "lon": "52.3216628255807", 
       "name": "bennebroek, Bennebroek, Schoollaan", 
       "id": "55241011"
     }, 
     {
       "lat": "4.59369684782427", 
       "lon": "52.3245918610376", 
       "name": "bennebroek, Bennebroek, Anemonenplein", 
       "id": "55247010"
     }, 
     {
       "lat": "4.52634094061659", 
       "lon": "52.2252149721336", 
       "name": "sassenheim, Sassenheim, Parklaan", 
       "id": "55540080"
     }, 
     {
       "lat": "4.51329148902133", 
       "lon": "52.2204272557238", 
       "name": "sassenheim, Sassenheim, Zuiderstraat", 
       "id": "55540090"
     }, 
     {
       "lat": "4.51957885780818", 
       "lon": "52.2237183799379", 
       "name": "sassenheim, Sassenheim, Raadhuis", 
       "id": "55540100"
     }, 
     {
       "lat": "4.51975883755538", 
       "lon": "52.223494995271", 
       "name": "sassenheim, Sassenheim, Raadhuis", 
       "id": "55540110"
     }, 
     {
       "lat": "4.51275219977666", 
       "lon": "52.2203154044403", 
       "name": "sassenheim, Sassenheim, Zuiderstraat", 
       "id": "55540120"
     }, 
     {
       "lat": "4.52418342070619", 
       "lon": "52.2232577619225", 
       "name": "sassenheim, Sassenheim, Menneweg", 
       "id": "55540130"
     }, 
     {
       "lat": "4.52939770352056", 
       "lon": "52.2276101117321", 
       "name": "sassenheim, Sassenheim, Parklaan", 
       "id": "55540150"
     }, 
     {
       "lat": "4.63213603554361", 
       "lon": "52.306076498069", 
       "name": "hoofddorp, Hoofddorp, Duinbeek", 
       "id": "56230030"
     }, 
     {
       "lat": "4.67690577419129", 
       "lon": "52.3443189548006", 
       "name": "ONBEKEND, Vijfhuizen", 
       "id": "56230080"
     }, 
     {
       "lat": "4.67645649138515", 
       "lon": "52.3448824959139", 
       "name": "ONBEKEND, Vijfhuizen", 
       "id": "56230090"
     }, 
     {
       "lat": "4.63736714623101", 
       "lon": "52.3097589145475", 
       "name": "hoofddorp, Hoofddorp, Floriande eiland 4", 
       "id": "56230100"
     }, 
     {
       "lat": "4.65218279874845", 
       "lon": "52.3200892362329", 
       "name": "hoofddorp, Hoofddorp, Schiermonnikoog", 
       "id": "56230110"
     }, 
     {
       "lat": "4.65222962156566", 
       "lon": "52.3199187555471", 
       "name": "hoofddorp, Hoofddorp, Schiermonnikoog", 
       "id": "56230120"
     }, 
     {
       "lat": "4.6479058909603", 
       "lon": "52.317087560259", 
       "name": "hoofddorp, Hoofddorp, Terschelling", 
       "id": "56230130"
     }, 
     {
       "lat": "4.64809713182859", 
       "lon": "52.3170528034276", 
       "name": "hoofddorp, Hoofddorp, Terschelling", 
       "id": "56230140"
     }, 
     {
       "lat": "4.64381718318963", 
       "lon": "52.3142666682712", 
       "name": "hoofddorp, Hoofddorp, Texel", 
       "id": "56230150"
     }, 
     {
       "lat": "4.6440233796146", 
       "lon": "52.3142140360481", 
       "name": "hoofddorp, Hoofddorp, Texel", 
       "id": "56230160"
     }, 
     {
       "lat": "4.64046623167013", 
       "lon": "52.3120794516138", 
       "name": "hoofddorp, Hoofddorp, Haringvliet", 
       "id": "56230170"
     }, 
     {
       "lat": "4.64081950617582", 
       "lon": "52.3120007894627", 
       "name": "hoofddorp, Hoofddorp, Haringvliet", 
       "id": "56230180"
     }, 
     {
       "lat": "4.65540308035533", 
       "lon": "52.3222663160885", 
       "name": "hoofddorp, Hoofddorp, Rottumeroog", 
       "id": "56230190"
     }, 
     {
       "lat": "4.65571033805938", 
       "lon": "52.3223131563123", 
       "name": "hoofddorp, Hoofddorp, Rottumeroog", 
       "id": "56230200"
     }, 
     {
       "lat": "4.65406836649843", 
       "lon": "52.3249274794178", 
       "name": "hoofddorp, Hoofddorp, Spaarne Ziekenhuis", 
       "id": "56230600"
     }, 
     {
       "lat": "4.65376168612038", 
       "lon": "52.3248446867221", 
       "name": "hoofddorp, Hoofddorp, Spaarne Ziekenhuis", 
       "id": "56230610"
     }, 
     {
       "lat": "4.65472825286127", 
       "lon": "52.3249405550119", 
       "name": "hoofddorp, Hoofddorp, Spaarne Ziekenhuis", 
       "id": "56230620"
     }, 
     {
       "lat": "4.63768911222336", 
       "lon": "52.309796907409", 
       "name": "hoofddorp, Hoofddorp, Floriande eiland 4", 
       "id": "56230630"
     }, 
     {
       "lat": "4.64865769051231", 
       "lon": "52.3292080503703", 
       "name": "cruquius, Cruquius, Spieringweg", 
       "id": "56232010"
     }, 
     {
       "lat": "4.63706487197263", 
       "lon": "52.3372152986408", 
       "name": "cruquius, Cruquius, Ringvaartbrug", 
       "id": "56232030"
     }, 
     {
       "lat": "4.6474055962628", 
       "lon": "52.3303956270842", 
       "name": "cruquius, Cruquius, Spieringweg", 
       "id": "56232060"
     }, 
     {
       "lat": "4.61207632053187", 
       "lon": "52.3170649171616", 
       "name": "zwaanshoek, Zwaanshoek, Bennebroekerdijk", 
       "id": "56237010"
     }, 
     {
       "lat": "4.61228005893195", 
       "lon": "52.3171561323178", 
       "name": "zwaanshoek, Zwaanshoek, Bennebroekerdijk", 
       "id": "56237020"
     }, 
     {
       "lat": "4.6141055912907", 
       "lon": "52.3117033594522", 
       "name": "zwaanshoek, Zwaanshoek, Hanepoel", 
       "id": "56237030"
     }, 
     {
       "lat": "4.61413225887779", 
       "lon": "52.3118563302468", 
       "name": "zwaanshoek, Zwaanshoek, Hanepoel", 
       "id": "56237040"
     }, 
     {
       "lat": "4.61761436870925", 
       "lon": "52.3106297033565", 
       "name": "zwaanshoek, Zwaanshoek, Supermarkt", 
       "id": "56237050"
     }, 
     {
       "lat": "4.61771358286021", 
       "lon": "52.310828085491", 
       "name": "zwaanshoek, Zwaanshoek, Supermarkt", 
       "id": "56237060"
     }, 
     {
       "lat": "4.62189344647678", 
       "lon": "52.3125000141256", 
       "name": "zwaanshoek, Zwaanshoek, Noppenstraat", 
       "id": "56237070"
     }, 
     {
       "lat": "4.62158675734162", 
       "lon": "52.3124261251109", 
       "name": "zwaanshoek, Zwaanshoek, Noppenstraat", 
       "id": "56237080"
     }, 
     {
       "lat": "4.64381163697626", 
       "lon": "52.3268677902092", 
       "name": "cruquius, Cruquius, Spieringweg", 
       "id": "56237090"
     }, 
     {
       "lat": "4.64410153927856", 
       "lon": "52.3270763349521", 
       "name": "cruquius, Cruquius, Spieringweg", 
       "id": "56237100"
     }, 
     {
       "lat": "4.62972094519478", 
       "lon": "52.3170084558655", 
       "name": "zwaanshoek, Zwaanshoek, Begraafplaats", 
       "id": "56237110"
     }, 
     {
       "lat": "4.63002752638991", 
       "lon": "52.3170913108294", 
       "name": "zwaanshoek, Zwaanshoek, Begraafplaats", 
       "id": "56237120"
     }, 
     {
       "lat": "4.67151619608906", 
       "lon": "52.3500117843594", 
       "name": "ONBEKEND, dummyfinancierwissel ZTG", 
       "id": "56239970"
     }, 
     {
       "lat": "4.72035604050877", 
       "lon": "52.3249961360476", 
       "name": "hoofddorp, Hoofddorp, Vijfhuizerweg", 
       "id": "56242010"
     }, 
     {
       "lat": "4.72032414137224", 
       "lon": "52.3251667266004", 
       "name": "hoofddorp, Hoofddorp, Vijfhuizerweg", 
       "id": "56242011"
     }, 
     {
       "lat": "4.71182086330562", 
       "lon": "52.3190696139376", 
       "name": "hoofddorp, Hoofddorp, Cornelia's Hoeve", 
       "id": "56242020"
     }, 
     {
       "lat": "4.73679215558043", 
       "lon": "52.3365382126632", 
       "name": "hoofddorp, Hoofddorp, Hoofdweg 271", 
       "id": "56242030"
     }, 
     {
       "lat": "4.73650004315883", 
       "lon": "52.3364467278262", 
       "name": "hoofddorp, Hoofddorp, Hoofdweg 271", 
       "id": "56242031"
     }, 
     {
       "lat": "4.75024284707866", 
       "lon": "52.3460306620969", 
       "name": "lijnden, Lijnden, Lijnden", 
       "id": "56242050"
     }, 
     {
       "lat": "4.74284769162166", 
       "lon": "52.3408765341311", 
       "name": "hoofddorp, Hoofddorp, Hoofdweg 199", 
       "id": "56242070"
     }, 
     {
       "lat": "4.74353288884174", 
       "lon": "52.3411858506588", 
       "name": "hoofddorp, Hoofddorp, Hoofdweg 199", 
       "id": "56242079"
     }, 
     {
       "lat": "4.66680486686801", 
       "lon": "52.3192624158974", 
       "name": "hoofddorp, Hoofddorp, Overbos", 
       "id": "56330560"
     }, 
     {
       "lat": "4.65474306851478", 
       "lon": "52.3249316587752", 
       "name": "hoofddorp, Hoofddorp, Spaarne Ziekenhuis", 
       "id": "56330580"
     }, 
     {
       "lat": "4.66863721216904", 
       "lon": "52.3184197039132", 
       "name": "hoofddorp, Hoofddorp, Overbos", 
       "id": "56330590"
     }, 
     {
       "lat": "4.65429683132913", 
       "lon": "52.3244165807626", 
       "name": "hoofddorp, Hoofddorp, Spaarne Ziekenhuis", 
       "id": "56330600"
     }, 
     {
       "lat": "4.6538330939786", 
       "lon": "52.3249619730256", 
       "name": "hoofddorp, Hoofddorp, Spaarne Ziekenhuis", 
       "id": "56330610"
     }, 
     {
       "lat": "4.66804710746608", 
       "lon": "52.3186318289977", 
       "name": "hoofddorp, Hoofddorp, Overbos", 
       "id": "56330620"
     }, 
     {
       "lat": "4.6672766420826", 
       "lon": "52.3191124926475", 
       "name": "hoofddorp, Hoofddorp, Overbos", 
       "id": "56330630"
     }, 
     {
       "lat": "4.66772264285456", 
       "lon": "52.3096868192658", 
       "name": "hoofddorp, Hoofddorp, Bornholm", 
       "id": "56330640"
     }, 
     {
       "lat": "4.66839188112787", 
       "lon": "52.3100144559191", 
       "name": "hoofddorp, Hoofddorp, Bornholm", 
       "id": "56330650"
     }, 
     {
       "lat": "4.66954933269393", 
       "lon": "52.3028131180571", 
       "name": "hoofddorp, Hoofddorp, Toolenburg", 
       "id": "56330660"
     }, 
     {
       "lat": "4.66892648822497", 
       "lon": "52.3032497484492", 
       "name": "hoofddorp, Hoofddorp, Toolenburg", 
       "id": "56330670"
     }, 
     {
       "lat": "4.68401243053605", 
       "lon": "52.2949725958501", 
       "name": "hoofddorp, Hoofddorp, Graan voor Visch", 
       "id": "56330680"
     }, 
     {
       "lat": "4.68336066482692", 
       "lon": "52.2954001418921", 
       "name": "hoofddorp, Hoofddorp, Graan voor Visch", 
       "id": "56330690"
     }, 
     {
       "lat": "4.69851013140639", 
       "lon": "52.2921368272487", 
       "name": "hoofddorp, Hoofddorp, Station", 
       "id": "56330710"
     }, 
     {
       "lat": "4.67793790673872", 
       "lon": "52.3137032276545", 
       "name": "hoofddorp, Hoofddorp, Houtwijkerveld", 
       "id": "56332020"
     }, 
     {
       "lat": "4.67860537420767", 
       "lon": "52.3132308658912", 
       "name": "hoofddorp, Hoofddorp, Houtwijkerveld", 
       "id": "56332030"
     }, 
     {
       "lat": "4.6871822257962", 
       "lon": "52.3087160511331", 
       "name": "hoofddorp, Hoofddorp, RK Kerk", 
       "id": "56332040"
     }, 
     {
       "lat": "4.68764326145477", 
       "lon": "52.3083053324001", 
       "name": "hoofddorp, Hoofddorp, RK Kerk", 
       "id": "56332050"
     }, 
     {
       "lat": "4.6920967020019", 
       "lon": "52.304826282246", 
       "name": "hoofddorp, Hoofddorp, Marktplein", 
       "id": "56332080"
     }, 
     {
       "lat": "4.69213717061315", 
       "lon": "52.305051219392", 
       "name": "hoofddorp, Hoofddorp, Marktplein", 
       "id": "56332090"
     }, 
     {
       "lat": "4.69944061715961", 
       "lon": "52.301157187188", 
       "name": "hoofddorp, Hoofddorp, Prins Hendriklaan", 
       "id": "56332101"
     }, 
     {
       "lat": "4.7000119287973", 
       "lon": "52.3011874723473", 
       "name": "hoofddorp, Hoofddorp, Prins Hendriklaan", 
       "id": "56332111"
     }, 
     {
       "lat": "4.70461599025879", 
       "lon": "52.2992457712893", 
       "name": "hoofddorp, Hoofddorp, Kalorama", 
       "id": "56332120"
     }, 
     {
       "lat": "4.70461847454299", 
       "lon": "52.2990840021419", 
       "name": "hoofddorp, Hoofddorp, Kalorama", 
       "id": "56332130"
     }, 
     {
       "lat": "4.66959318188337", 
       "lon": "52.3064535206691", 
       "name": "hoofddorp, Hoofddorp, Asserweg", 
       "id": "56332250"
     }, 
     {
       "lat": "4.66947458449851", 
       "lon": "52.3065336928861", 
       "name": "hoofddorp, Hoofddorp, Asserweg", 
       "id": "56332260"
     }, 
     {
       "lat": "4.64969684648082", 
       "lon": "52.3090365096325", 
       "name": "hoofddorp, Hoofddorp, Henri Didonweg", 
       "id": "56332270"
     }, 
     {
       "lat": "4.64940405066557", 
       "lon": "52.3090077194581", 
       "name": "hoofddorp, Hoofddorp, Henri Didonweg", 
       "id": "56332280"
     }, 
     {
       "lat": "4.67395338323783", 
       "lon": "52.3061203774497", 
       "name": "hoofddorp, Hoofddorp, Kelloggstraat", 
       "id": "56332290"
     }, 
     {
       "lat": "4.67396674632067", 
       "lon": "52.3062013499057", 
       "name": "hoofddorp, Hoofddorp, Kelloggstraat", 
       "id": "56332300"
     }, 
     {
       "lat": "4.707931369272", 
       "lon": "52.303902651527", 
       "name": "hoofddorp, Hoofddorp, Boslaan", 
       "id": "56332320"
     }, 
     {
       "lat": "4.67850484852126", 
       "lon": "52.3029839689026", 
       "name": "hoofddorp, Hoofddorp, WKC Lutulistraat", 
       "id": "56332330"
     }, 
     {
       "lat": "4.67840179674741", 
       "lon": "52.3030103152597", 
       "name": "hoofddorp, Hoofddorp, WKC Lutulistraat", 
       "id": "56332340"
     }, 
     {
       "lat": "4.70098128700678", 
       "lon": "52.3115202697096", 
       "name": "hoofddorp, Hoofddorp, Wijkermeerstraat", 
       "id": "56332440"
     }, 
     {
       "lat": "4.70097892737516", 
       "lon": "52.3116730512211", 
       "name": "hoofddorp, Hoofddorp, Wijkermeerstraat", 
       "id": "56332450"
     }, 
     {
       "lat": "4.69221933772991", 
       "lon": "52.301672223864", 
       "name": "hoofddorp, Hoofddorp, Burg. van Stamplein", 
       "id": "56332460"
     }, 
     {
       "lat": "4.69150989697135", 
       "lon": "52.3020365595669", 
       "name": "hoofddorp, Hoofddorp, Burg. van Stamplein", 
       "id": "56332461"
     }, 
     {
       "lat": "4.69251759188289", 
       "lon": "52.3013504090852", 
       "name": "hoofddorp, Hoofddorp, Burg. van Stamplein", 
       "id": "56332470"
     }, 
     {
       "lat": "4.69185143527842", 
       "lon": "52.3017599409725", 
       "name": "hoofddorp, Hoofddorp, Burg. van Stamplein", 
       "id": "56332471"
     }, 
     {
       "lat": "4.68375548247142", 
       "lon": "52.3010199853388", 
       "name": "hoofddorp, Hoofddorp, Wallenbergstraat", 
       "id": "56332480"
     }, 
     {
       "lat": "4.68384642689091", 
       "lon": "52.3008317785846", 
       "name": "hoofddorp, Hoofddorp, Wallenbergstraat", 
       "id": "56332490"
     }, 
     {
       "lat": "4.69188970540298", 
       "lon": "52.2965021964944", 
       "name": "hoofddorp, Hoofddorp, Nieuweweg", 
       "id": "56332540"
     }, 
     {
       "lat": "4.69144686624227", 
       "lon": "52.2966973274399", 
       "name": "hoofddorp, Hoofddorp, Nieuweweg", 
       "id": "56332550"
     }, 
     {
       "lat": "4.63933555657009", 
       "lon": "52.307811991499", 
       "name": "hoofddorp, Hoofddorp, Floriande Centrum", 
       "id": "56332560"
     }, 
     {
       "lat": "4.63942307331461", 
       "lon": "52.3078395089181", 
       "name": "hoofddorp, Hoofddorp, Floriande Centrum", 
       "id": "56332570"
     }, 
     {
       "lat": "4.69828248148188", 
       "lon": "52.29263882843", 
       "name": "hoofddorp, Hoofddorp, Station", 
       "id": "56332580"
     }, 
     {
       "lat": "4.69783915140621", 
       "lon": "52.2928699322832", 
       "name": "hoofddorp, Hoofddorp, Station", 
       "id": "56332583"
     }, 
     {
       "lat": "4.69840112907828", 
       "lon": "52.2925496397766", 
       "name": "hoofddorp, Hoofddorp, Station", 
       "id": "56332584"
     }, 
     {
       "lat": "4.6970357753427", 
       "lon": "52.3087380094704", 
       "name": "hoofddorp, Hoofddorp, Beemsterstraat", 
       "id": "56332600"
     }, 
     {
       "lat": "4.69682980640906", 
       "lon": "52.3087817471826", 
       "name": "hoofddorp, Hoofddorp, Beemsterstraat", 
       "id": "56332610"
     }, 
     {
       "lat": "4.67030224767006", 
       "lon": "52.2897671012545", 
       "name": "hoofddorp, Hoofddorp, De President", 
       "id": "56332660"
     }, 
     {
       "lat": "4.6727593057393", 
       "lon": "52.2910133315258", 
       "name": "hoofddorp, Hoofddorp, De President", 
       "id": "56332670"
     }, 
     {
       "lat": "4.67784014213777", 
       "lon": "52.2950256089056", 
       "name": "hoofddorp, Hoofddorp, Jadelaan", 
       "id": "56332680"
     }, 
     {
       "lat": "4.67698682914356", 
       "lon": "52.2943014465542", 
       "name": "hoofddorp, Hoofddorp, Jadelaan", 
       "id": "56332690"
     }, 
     {
       "lat": "4.68456741910438", 
       "lon": "52.2997395303319", 
       "name": "hoofddorp, Hoofddorp, Graan voor Visch", 
       "id": "56332700"
     }, 
     {
       "lat": "4.68416620156093", 
       "lon": "52.2991529265091", 
       "name": "hoofddorp, Hoofddorp, Graan voor Visch", 
       "id": "56332710"
     }, 
     {
       "lat": "4.70514714907505", 
       "lon": "52.3018912988276", 
       "name": "hoofddorp, Hoofddorp, Koning Willem I laan", 
       "id": "56332720"
     }, 
     {
       "lat": "4.70605915691701", 
       "lon": "52.3026515443241", 
       "name": "hoofddorp, Hoofddorp, Koning Willem I laan", 
       "id": "56332730"
     }, 
     {
       "lat": "4.71106358463939", 
       "lon": "52.3187147585275", 
       "name": "hoofddorp, Hoofddorp, Cornelia's Hoeve", 
       "id": "56332770"
     }, 
     {
       "lat": "4.65753439606372", 
       "lon": "52.3157452224083", 
       "name": "hoofddorp, Hoofddorp, WKC 't Paradijs", 
       "id": "56332800"
     }, 
     {
       "lat": "4.65728805427278", 
       "lon": "52.3155639428528", 
       "name": "hoofddorp, Hoofddorp, WKC 't Paradijs", 
       "id": "56332810"
     }, 
     {
       "lat": "4.66106988939437", 
       "lon": "52.3192722902006", 
       "name": "hoofddorp, Hoofddorp, Corversbos", 
       "id": "56332830"
     }, 
     {
       "lat": "4.65854898424007", 
       "lon": "52.3075364550643", 
       "name": "hoofddorp, Hoofddorp, Breeburgsingel", 
       "id": "56332840"
     }, 
     {
       "lat": "4.65851089416827", 
       "lon": "52.3071767005314", 
       "name": "hoofddorp, Hoofddorp, Breeburgsingel", 
       "id": "56332850"
     }, 
     {
       "lat": "4.69293331085187", 
       "lon": "52.3085252514287", 
       "name": "hoofddorp, Hoofddorp, Stationsweg", 
       "id": "56332890"
     }, 
     {
       "lat": "4.69362691936403", 
       "lon": "52.3082417061021", 
       "name": "hoofddorp, Hoofddorp, Stationsweg", 
       "id": "56332900"
     }, 
     {
       "lat": "4.70072462328968", 
       "lon": "52.3053530406415", 
       "name": "hoofddorp, Hoofddorp, Van den Berghlaan", 
       "id": "56332910"
     }, 
     {
       "lat": "4.70034510179033", 
       "lon": "52.3052429815135", 
       "name": "hoofddorp, Hoofddorp, Van den Berghlaan", 
       "id": "56332920"
     }, 
     {
       "lat": "4.65296609662869", 
       "lon": "52.3117442614949", 
       "name": "hoofddorp, Hoofddorp, Liesbos", 
       "id": "56332930"
     }, 
     {
       "lat": "4.65318574585754", 
       "lon": "52.3117636008276", 
       "name": "hoofddorp, Hoofddorp, Liesbos", 
       "id": "56332940"
     }, 
     {
       "lat": "4.69009435757841", 
       "lon": "52.3100275185644", 
       "name": "hoofddorp, Hoofddorp, De Meerstede", 
       "id": "56332950"
     }, 
     {
       "lat": "4.68984325963062", 
       "lon": "52.3101428818679", 
       "name": "hoofddorp, Hoofddorp, De Meerstede", 
       "id": "56332960"
     }, 
     {
       "lat": "4.68705318627566", 
       "lon": "52.3113217978298", 
       "name": "hoofddorp, Hoofddorp, Oranjestraat", 
       "id": "56332970"
     }, 
     {
       "lat": "4.68624700345639", 
       "lon": "52.3112990468651", 
       "name": "hoofddorp, Hoofddorp, Oranjestraat", 
       "id": "56332980"
     }, 
     {
       "lat": "4.65884985901732", 
       "lon": "52.3034937087547", 
       "name": "hoofddorp, Hoofddorp, Rustenburgpark", 
       "id": "56332990"
     }, 
     {
       "lat": "4.65881472424151", 
       "lon": "52.3047428245831", 
       "name": "hoofddorp, Hoofddorp, Rustenburgpark", 
       "id": "56333000"
     }, 
     {
       "lat": "4.66134618586031", 
       "lon": "52.3194177935141", 
       "name": "hoofddorp, Hoofddorp, Corversbos", 
       "id": "56333030"
     }, 
     {
       "lat": "4.66392897658221", 
       "lon": "52.3004150331179", 
       "name": "hoofddorp, Hoofddorp, Aletta Jacobsdreef", 
       "id": "56333060"
     }, 
     {
       "lat": "4.66390038912313", 
       "lon": "52.3003699182487", 
       "name": "hoofddorp, Hoofddorp, Aletta Jacobsdreef", 
       "id": "56333070"
     }, 
     {
       "lat": "4.675908313574", 
       "lon": "52.2984923597541", 
       "name": "hoofddorp, Hoofddorp, Joke Smitstraat", 
       "id": "56333080"
     }, 
     {
       "lat": "4.67589609977043", 
       "lon": "52.2983394903421", 
       "name": "hoofddorp, Hoofddorp, Joke Smitstraat", 
       "id": "56333090"
     }, 
     {
       "lat": "4.67034304125217", 
       "lon": "52.2972363847955", 
       "name": "hoofddorp, Hoofddorp, Mary Zeldenruststr.", 
       "id": "56333100"
     }, 
     {
       "lat": "4.67065188046814", 
       "lon": "52.2971753406419", 
       "name": "hoofddorp, Hoofddorp, Mary Zeldenruststr.", 
       "id": "56333110"
     }, 
     {
       "lat": "4.70134274055707", 
       "lon": "52.2957035451562", 
       "name": "hoofddorp, Hoofddorp, Saturnusstraat", 
       "id": "56333120"
     }, 
     {
       "lat": "4.70132309059658", 
       "lon": "52.2960269984559", 
       "name": "hoofddorp, Hoofddorp, Saturnusstraat", 
       "id": "56333130"
     }, 
     {
       "lat": "4.70494121279409", 
       "lon": "52.2981151636041", 
       "name": "hoofddorp, Hoofddorp, Jupiterstraat", 
       "id": "56333160"
     }, 
     {
       "lat": "4.70451818058341", 
       "lon": "52.2979779025457", 
       "name": "hoofddorp, Hoofddorp, Jupiterstraat", 
       "id": "56333170"
     }, 
     {
       "lat": "4.70540721358735", 
       "lon": "52.3059643455385", 
       "name": "hoofddorp, Hoofddorp, Arnolduspark", 
       "id": "56333290"
     }, 
     {
       "lat": "4.70511012507976", 
       "lon": "52.3062142953453", 
       "name": "hoofddorp, Hoofddorp, Arnolduspark", 
       "id": "56333300"
     }, 
     {
       "lat": "4.68228195464981", 
       "lon": "52.2959419838737", 
       "name": "hoofddorp, Hoofddorp, Opaallaan", 
       "id": "56333310"
     }, 
     {
       "lat": "4.66453525761117", 
       "lon": "52.3055059469567", 
       "name": "hoofddorp, Hoofddorp, Zwembad", 
       "id": "56337030"
     }, 
     {
       "lat": "4.66454728802379", 
       "lon": "52.3056678043634", 
       "name": "hoofddorp, Hoofddorp, Zwembad", 
       "id": "56337040"
     }, 
     {
       "lat": "4.65567172619901", 
       "lon": "52.3068445931941", 
       "name": "hoofddorp, Hoofddorp, IJweg/Altenburg", 
       "id": "56337050"
     }, 
     {
       "lat": "4.65460276593265", 
       "lon": "52.3076468963505", 
       "name": "hoofddorp, Hoofddorp, IJweg/Leenderbos", 
       "id": "56337060"
     }, 
     {
       "lat": "4.62682879569333", 
       "lon": "52.2614706812511", 
       "name": "nieuw-vennep, Nieuw-Vennep, Zuiderdreef", 
       "id": "56432090"
     }, 
     {
       "lat": "4.62199397619021", 
       "lon": "52.2640819775791", 
       "name": "nieuw-vennep, Nieuw-Vennep, Westerkim", 
       "id": "56432110"
     }, 
     {
       "lat": "4.62492135612387", 
       "lon": "52.2676422053223", 
       "name": "nieuw-vennep, Nieuw-Vennep, Westerdreef", 
       "id": "56432120"
     }, 
     {
       "lat": "4.62569064822429", 
       "lon": "52.268060616678", 
       "name": "nieuw-vennep, Nieuw-Vennep, Westerdreef", 
       "id": "56432130"
     }, 
     {
       "lat": "4.62168591942837", 
       "lon": "52.2641069469087", 
       "name": "nieuw-vennep, Nieuw-Vennep, Westerkim", 
       "id": "56432140"
     }, 
     {
       "lat": "4.62573665463739", 
       "lon": "52.2619490068682", 
       "name": "nieuw-vennep, Nieuw-Vennep, Zuiderdreef", 
       "id": "56432160"
     }, 
     {
       "lat": "4.62081968423339", 
       "lon": "52.2557154258993", 
       "name": "nieuw-vennep, Nieuw-Vennep, Landei", 
       "id": "56432270"
     }, 
     {
       "lat": "4.62471687311601", 
       "lon": "52.2582033794492", 
       "name": "nieuw-vennep, Nieuw-Vennep, Landei", 
       "id": "56432280"
     }, 
     {
       "lat": "4.60532759131965", 
       "lon": "52.2446753685509", 
       "name": "abbenes, Abbenes, Lisserweg/Hoofdweg", 
       "id": "56432300"
     }, 
     {
       "lat": "4.64218346151594", 
       "lon": "52.2700082843987", 
       "name": "nieuw-vennep, Nieuw-Vennep, Hoofdweg 1194", 
       "id": "56432460"
     }, 
     {
       "lat": "4.64184848547634", 
       "lon": "52.2698893275228", 
       "name": "nieuw-vennep, Nieuw-Vennep, Hoofdweg 1194", 
       "id": "56432469"
     }, 
     {
       "lat": "4.65201567820966", 
       "lon": "52.2770086320313", 
       "name": "nieuw-vennep, Nieuw-Vennep, Hoeve Klaverblad", 
       "id": "56432470"
     }, 
     {
       "lat": "4.63789579917437", 
       "lon": "52.2688396944397", 
       "name": "nieuw-vennep, Nieuw-Vennep, Noorderdreef", 
       "id": "56432540"
     }, 
     {
       "lat": "4.63773678107167", 
       "lon": "52.2687128530925", 
       "name": "nieuw-vennep, Nieuw-Vennep, Noorderdreef", 
       "id": "56432550"
     }, 
     {
       "lat": "4.63235199378493", 
       "lon": "52.2717794740027", 
       "name": "nieuw-vennep, Nieuw-Vennep, Lucas Bolsstraat", 
       "id": "56432560"
     }, 
     {
       "lat": "4.63245682999537", 
       "lon": "52.2716453222658", 
       "name": "nieuw-vennep, Nieuw-Vennep, Lucas Bolsstraat", 
       "id": "56432570"
     }, 
     {
       "lat": "4.62799032896425", 
       "lon": "52.2698011242033", 
       "name": "nieuw-vennep, Nieuw-Vennep, Raiffeisenstraat", 
       "id": "56432580"
     }, 
     {
       "lat": "4.62870185618659", 
       "lon": "52.2701742040029", 
       "name": "nieuw-vennep, Nieuw-Vennep, Raiffeisenstraat", 
       "id": "56432590"
     }, 
     {
       "lat": "4.61675810953012", 
       "lon": "52.2669780830132", 
       "name": "nieuw-vennep, Nieuw-Vennep, Laan van Berlioz", 
       "id": "56432600"
     }, 
     {
       "lat": "4.6171805746538", 
       "lon": "52.2671156577168", 
       "name": "nieuw-vennep, Nieuw-Vennep, Laan van Berlioz", 
       "id": "56432610"
     }, 
     {
       "lat": "4.65616172811457", 
       "lon": "52.279730759282", 
       "name": "nieuw-vennep, Nieuw-Vennep, Hoeve Klaverblad", 
       "id": "56432630"
     }, 
     {
       "lat": "4.62602519329549", 
       "lon": "52.2733387790993", 
       "name": "nieuw-vennep, Nieuw-Vennep, Laan van Norma", 
       "id": "56432650"
     }, 
     {
       "lat": "4.62574791378663", 
       "lon": "52.2732740766101", 
       "name": "nieuw-vennep, Nieuw-Vennep, Laan van Norma", 
       "id": "56432660"
     }, 
     {
       "lat": "4.62189670090385", 
       "lon": "52.2705887299326", 
       "name": "nieuw-vennep, Nieuw-Vennep, Getsewoud Centrum", 
       "id": "56432680"
     }, 
     {
       "lat": "4.6222317830835", 
       "lon": "52.2706987561609", 
       "name": "nieuw-vennep, Nieuw-Vennep, Getsewoud Centrum", 
       "id": "56432690"
     }, 
     {
       "lat": "4.61366089496489", 
       "lon": "52.2648007068614", 
       "name": "nieuw-vennep, Nieuw-Vennep, Laan van Bizet", 
       "id": "56432700"
     }, 
     {
       "lat": "4.6135900015027", 
       "lon": "52.2646654211965", 
       "name": "nieuw-vennep, Nieuw-Vennep, Laan van Bizet", 
       "id": "56432710"
     }, 
     {
       "lat": "4.60131761245637", 
       "lon": "52.2420691625131", 
       "name": "nieuw-vennep, Nieuw-Vennep, Lisserweg/Hoofdweg", 
       "id": "56532010"
     }, 
     {
       "lat": "4.59455347259223", 
       "lon": "52.2371164336268", 
       "name": "abbenes, Abbenes, Langerak", 
       "id": "56532020"
     }, 
     {
       "lat": "4.59284410681806", 
       "lon": "52.2360982761248", 
       "name": "abbenes, Abbenes, Langerak", 
       "id": "56532030"
     }, 
     {
       "lat": "4.59058710957572", 
       "lon": "52.2346000280422", 
       "name": "abbenes, Abbenes, Doctor Heijebrug", 
       "id": "56532040"
     }, 
     {
       "lat": "4.59009072187244", 
       "lon": "52.2345247740705", 
       "name": "abbenes, Abbenes, Doctor Heijebrug", 
       "id": "56532050"
     }, 
     {
       "lat": "4.57623594190457", 
       "lon": "52.2284263536427", 
       "name": "abbenes, Abbenes, Viadukt A44", 
       "id": "56532060"
     }, 
     {
       "lat": "4.57488238806408", 
       "lon": "52.2280035950832", 
       "name": "abbenes, Abbenes, Viadukt A44", 
       "id": "56532070"
     }, 
     {
       "lat": "4.87664109908506", 
       "lon": "52.3693105350931", 
       "name": "amsterdam, Amsterdam, Marnixstraat", 
       "id": "57000073"
     }, 
     {
       "lat": "4.86503992589973", 
       "lon": "52.3519585250044", 
       "name": "amsterdam, Amsterdam, Valeriusplein", 
       "id": "57002150"
     }, 
     {
       "lat": "4.85761733648162", 
       "lon": "52.3491393386562", 
       "name": "amsterdam, Amsterdam, Haarlemmermeerstation", 
       "id": "57002170"
     }, 
     {
       "lat": "4.85704677065489", 
       "lon": "52.3502153170193", 
       "name": "amsterdam, Amsterdam, Haarlemmermeerstation", 
       "id": "57002171"
     }, 
     {
       "lat": "4.86417854598953", 
       "lon": "52.351568248042", 
       "name": "amsterdam, Amsterdam, Valeriusplein", 
       "id": "57002200"
     }, 
     {
       "lat": "4.898102179611", 
       "lon": "52.3778405889354", 
       "name": "amsterdam, Amsterdam, Centraal Station", 
       "id": "57002330"
     }, 
     {
       "lat": "4.897870087644", 
       "lon": "52.3775789868774", 
       "name": "amsterdam, Amsterdam, Centraal Station", 
       "id": "57002340"
     }, 
     {
       "lat": "4.87001570982377", 
       "lon": "52.3532116939781", 
       "name": "amsterdam, Amsterdam, Emmastraat", 
       "id": "57002370"
     }, 
     {
       "lat": "4.86963766420501", 
       "lon": "52.3529044577735", 
       "name": "amsterdam, Amsterdam, Emmastraat", 
       "id": "57002380"
     }, 
     {
       "lat": "4.87970262981269", 
       "lon": "52.3660971039787", 
       "name": "amsterdam, Amsterdam, Raamplein", 
       "id": "57002390"
     }, 
     {
       "lat": "4.87984625921215", 
       "lon": "52.3663763391552", 
       "name": "amsterdam, Amsterdam, Raamplein", 
       "id": "57002400"
     }, 
     {
       "lat": "4.88127504253334", 
       "lon": "52.3633985270206", 
       "name": "amsterdam, Amsterdam, Leidseplein", 
       "id": "57002410"
     }, 
     {
       "lat": "4.87963461243806", 
       "lon": "52.3630589591196", 
       "name": "amsterdam, Amsterdam, Leidseplein", 
       "id": "57002412"
     }, 
     {
       "lat": "4.88172881211286", 
       "lon": "52.3635173058537", 
       "name": "amsterdam, Amsterdam, Leidseplein", 
       "id": "57002420"
     }, 
     {
       "lat": "4.87851643116822", 
       "lon": "52.3555853463673", 
       "name": "amsterdam, Amsterdam, Museumplein", 
       "id": "57002450"
     }, 
     {
       "lat": "4.87958433272108", 
       "lon": "52.3559045018509", 
       "name": "amsterdam, Amsterdam, Museumplein", 
       "id": "57002460"
     }, 
     {
       "lat": "4.87635152542144", 
       "lon": "52.3549289051924", 
       "name": "amsterdam, Amsterdam, Jacob Obrechtstraat", 
       "id": "57002510"
     }, 
     {
       "lat": "4.87601693691861", 
       "lon": "52.3546668159501", 
       "name": "amsterdam, Amsterdam, Jacob Obrechtstraat", 
       "id": "57002520"
     }, 
     {
       "lat": "4.89272097394866", 
       "lon": "52.3757510689657", 
       "name": "amsterdam, Amsterdam, Nieuwezijds Kolk", 
       "id": "57002530"
     }, 
     {
       "lat": "4.89372892388194", 
       "lon": "52.376231622055", 
       "name": "amsterdam, Amsterdam, Nieuwezijds Kolk", 
       "id": "57002540"
     }, 
     {
       "lat": "4.89123769939177", 
       "lon": "52.3744416482836", 
       "name": "amsterdam, Amsterdam, Dam", 
       "id": "57002550"
     }, 
     {
       "lat": "4.8900776589802", 
       "lon": "52.3731245782283", 
       "name": "amsterdam, Amsterdam, Dam", 
       "id": "57002560"
     }, 
     {
       "lat": "4.88360511456969", 
       "lon": "52.3741218257723", 
       "name": "amsterdam, Amsterdam, Westermarkt", 
       "id": "57002570"
     }, 
     {
       "lat": "4.88441417301138", 
       "lon": "52.3739994360357", 
       "name": "amsterdam, Amsterdam, Westermarkt", 
       "id": "57002580"
     }, 
     {
       "lat": "4.87610709821161", 
       "lon": "52.3723281058802", 
       "name": "amsterdam, Amsterdam, Marnixstraat", 
       "id": "57002590"
     }, 
     {
       "lat": "4.87700176488132", 
       "lon": "52.3724218415619", 
       "name": "amsterdam, Amsterdam, Marnixstraat", 
       "id": "57002600"
     }, 
     {
       "lat": "4.87747718199417", 
       "lon": "52.3693860393286", 
       "name": "amsterdam, Amsterdam, Elandsgracht", 
       "id": "57002610"
     }, 
     {
       "lat": "4.87748752740891", 
       "lon": "52.3697635682683", 
       "name": "amsterdam, Amsterdam, Elandsgracht", 
       "id": "57002620"
     }, 
     {
       "lat": "4.88338532765922", 
       "lon": "52.3598573713188", 
       "name": "amsterdam, Amsterdam, Hobbemastraat", 
       "id": "57002630"
     }, 
     {
       "lat": "4.88344037248339", 
       "lon": "52.3601811641221", 
       "name": "amsterdam, Amsterdam, Hobbemastraat", 
       "id": "57002640"
     }, 
     {
       "lat": "4.84718135025968", 
       "lon": "52.3781585785976", 
       "name": "amsterdam, Amsterdam, Bos en Lommerplein", 
       "id": "57130310"
     }, 
     {
       "lat": "4.84524660053578", 
       "lon": "52.3778441565609", 
       "name": "amsterdam, Amsterdam, Bos en Lommerplein", 
       "id": "57130320"
     }, 
     {
       "lat": "4.83473626512359", 
       "lon": "52.3856957990603", 
       "name": "amsterdam, Amsterdam, Arlandaweg", 
       "id": "57130350"
     }, 
     {
       "lat": "4.83535360692293", 
       "lon": "52.3856627265167", 
       "name": "amsterdam, Amsterdam, Arlandaweg", 
       "id": "57130360"
     }, 
     {
       "lat": "4.8468419255331", 
       "lon": "52.3469515421488", 
       "name": "amsterdam, Amsterdam, Aalsmeerplein", 
       "id": "57132040"
     }, 
     {
       "lat": "4.84624112029754", 
       "lon": "52.346876895281", 
       "name": "amsterdam, Amsterdam, Aalsmeerplein", 
       "id": "57132050"
     }, 
     {
       "lat": "4.83893157852911", 
       "lon": "52.3469511129569", 
       "name": "amsterdam, Amsterdam, Maassluisstraat", 
       "id": "57132080"
     }, 
     {
       "lat": "4.83838748710594", 
       "lon": "52.3470384690882", 
       "name": "amsterdam, Amsterdam, Maassluisstraat", 
       "id": "57132090"
     }, 
     {
       "lat": "4.8337661556281", 
       "lon": "52.3469090957233", 
       "name": "amsterdam, Amsterdam, Ottho Heldringstraat", 
       "id": "57132100"
     }, 
     {
       "lat": "4.8331196651746", 
       "lon": "52.3469689854045", 
       "name": "amsterdam, Amsterdam, Ottho Heldringstraat", 
       "id": "57132110"
     }, 
     {
       "lat": "4.8581337780254", 
       "lon": "52.350139290975", 
       "name": "amsterdam, Amsterdam, C.Krusemanstraat", 
       "id": "57132130"
     }, 
     {
       "lat": "4.82791359691173", 
       "lon": "52.3443290485504", 
       "name": "amsterdam, Amsterdam, Henk Sneevlietweg", 
       "id": "57132140"
     }, 
     {
       "lat": "4.85697604086236", 
       "lon": "52.3512216304951", 
       "name": "amsterdam, Amsterdam, Zeilstraat", 
       "id": "57132200"
     }, 
     {
       "lat": "4.84935097310343", 
       "lon": "52.3506299847783", 
       "name": "amsterdam, Amsterdam, Hoofddorpplein", 
       "id": "57132230"
     }, 
     {
       "lat": "4.84955448280097", 
       "lon": "52.3507926893442", 
       "name": "amsterdam, Amsterdam, Hoofddorpplein", 
       "id": "57132240"
     }, 
     {
       "lat": "4.84242503605015", 
       "lon": "52.3469043303563", 
       "name": "amsterdam, Amsterdam, Naaldwijkstraat", 
       "id": "57132250"
     }, 
     {
       "lat": "4.84264615536551", 
       "lon": "52.3468244578789", 
       "name": "amsterdam, Amsterdam, Naaldwijkstraat", 
       "id": "57132260"
     }, 
     {
       "lat": "4.82889435831158", 
       "lon": "52.3468592506526", 
       "name": "amsterdam, Amsterdam, Aletta Jacobslaan", 
       "id": "57132280"
     }, 
     {
       "lat": "4.82854102499815", 
       "lon": "52.3469474612855", 
       "name": "amsterdam, Amsterdam, Aletta Jacobslaan", 
       "id": "57132290"
     }, 
     {
       "lat": "4.87728938875471", 
       "lon": "52.3486774708155", 
       "name": "amsterdam, Amsterdam, Hervormd Lyceum", 
       "id": "57140010"
     }, 
     {
       "lat": "4.87732557006626", 
       "lon": "52.3493606965198", 
       "name": "amsterdam, Amsterdam, Hervormd Lyceum", 
       "id": "57140020"
     }, 
     {
       "lat": "4.88292181038637", 
       "lon": "52.3450975099667", 
       "name": "amsterdam, Amsterdam, Vossius Gymnasium", 
       "id": "57140030"
     }, 
     {
       "lat": "4.88249553134817", 
       "lon": "52.3451586072514", 
       "name": "amsterdam, Amsterdam, Vossius Gymnasium", 
       "id": "57140040"
     }, 
     {
       "lat": "4.86872224297852", 
       "lon": "52.3395446234136", 
       "name": "amsterdam, Amsterdam, Strawinskylaan", 
       "id": "57140250"
     }, 
     {
       "lat": "4.87696149344601", 
       "lon": "52.3350685679996", 
       "name": "amsterdam, Amsterdam, W. van Weldammelaan", 
       "id": "57140300"
     }, 
     {
       "lat": "4.87646411688487", 
       "lon": "52.3349405933086", 
       "name": "amsterdam, Amsterdam, W. van Weldammelaan", 
       "id": "57140310"
     }, 
     {
       "lat": "4.87728986742617", 
       "lon": "52.3371371737717", 
       "name": "amsterdam, Amsterdam, Gustav Mahlerlaan", 
       "id": "57140320"
     }, 
     {
       "lat": "4.87667126794963", 
       "lon": "52.3373412256174", 
       "name": "amsterdam, Amsterdam, Gustav Mahlerlaan", 
       "id": "57140330"
     }, 
     {
       "lat": "4.86020328829561", 
       "lon": "52.3353007063509", 
       "name": "amsterdam, Amsterdam, VU Medisch Centrum", 
       "id": "57142030"
     }, 
     {
       "lat": "4.85756816316381", 
       "lon": "52.3225082770214", 
       "name": "amsterdam, Amsterdam, Kalfjesl./Amstelv.wg", 
       "id": "57142040"
     }, 
     {
       "lat": "4.86964638033932", 
       "lon": "52.3320169012864", 
       "name": "amsterdam, Amsterdam, A.J.Ernststraat", 
       "id": "57142070"
     }, 
     {
       "lat": "4.86986520445307", 
       "lon": "52.3245669700866", 
       "name": "amsterdam, Amsterdam, van Boshuizenstraat", 
       "id": "57142100"
     }, 
     {
       "lat": "4.86982116705449", 
       "lon": "52.3321255192134", 
       "name": "amsterdam, Amsterdam, A.J.Ernststraat", 
       "id": "57142120"
     }, 
     {
       "lat": "4.85713528559652", 
       "lon": "52.3489484375323", 
       "name": "amsterdam, Amsterdam, Haarlemmermeerstation", 
       "id": "57142160"
     }, 
     {
       "lat": "4.8768249225324", 
       "lon": "52.3431210289827", 
       "name": "amsterdam, Amsterdam, Prinses Irenestraat", 
       "id": "57142170"
     }, 
     {
       "lat": "4.87669895447506", 
       "lon": "52.3425902071104", 
       "name": "amsterdam, Amsterdam, Prinses Irenestraat", 
       "id": "57142210"
     }, 
     {
       "lat": "4.87445798155623", 
       "lon": "52.3409537318379", 
       "name": "amsterdam, Amsterdam, Station Zuid", 
       "id": "57142220"
     }, 
     {
       "lat": "4.87397459619246", 
       "lon": "52.3408797342901", 
       "name": "amsterdam, Amsterdam, Station Zuid", 
       "id": "57142225"
     }, 
     {
       "lat": "4.87356561808241", 
       "lon": "52.3407161799474", 
       "name": "amsterdam, Amsterdam, Station Zuid", 
       "id": "57142230"
     }, 
     {
       "lat": "4.86939447236662", 
       "lon": "52.3221651652103", 
       "name": "amsterdam, Amsterdam, Kalfjeslaan/Beneluxb.", 
       "id": "57142250"
     }, 
     {
       "lat": "4.86787860933524", 
       "lon": "52.3351458961265", 
       "name": "amsterdam, Amsterdam, De Boelelaan/VU", 
       "id": "57142260"
     }, 
     {
       "lat": "4.86877067871922", 
       "lon": "52.3240858251516", 
       "name": "amsterdam, Amsterdam, van Boshuizenstraat", 
       "id": "57142280"
     }, 
     {
       "lat": "4.857605912183", 
       "lon": "52.326723731926", 
       "name": "amsterdam, Amsterdam, Van Nijenrodeweg", 
       "id": "57142340"
     }, 
     {
       "lat": "4.85741093369769", 
       "lon": "52.3270823715214", 
       "name": "amsterdam, Amsterdam, Van Nijenrodeweg", 
       "id": "57142350"
     }, 
     {
       "lat": "4.87703477318132", 
       "lon": "52.3248587488688", 
       "name": "amsterdam, Amsterdam, Backershagen", 
       "id": "57142510"
     }, 
     {
       "lat": "4.87515945622403", 
       "lon": "52.3246619037661", 
       "name": "amsterdam, Amsterdam, Backershagen", 
       "id": "57142520"
     }, 
     {
       "lat": "4.86831956663445", 
       "lon": "52.3401001010488", 
       "name": "amsterdam, Amsterdam, Strawinskylaan", 
       "id": "57142530"
     }, 
     {
       "lat": "4.87637858996361", 
       "lon": "52.3321719851116", 
       "name": "amsterdam, Amsterdam, Gelderlandplein", 
       "id": "57142550"
     }, 
     {
       "lat": "4.87661424521887", 
       "lon": "52.332092112083", 
       "name": "amsterdam, Amsterdam, Gelderlandplein", 
       "id": "57142560"
     }, 
     {
       "lat": "4.85736681432026", 
       "lon": "52.3406178012711", 
       "name": "amsterdam, Amsterdam, IJsbaanpad", 
       "id": "57142570"
     }, 
     {
       "lat": "4.85772110105392", 
       "lon": "52.3416709580367", 
       "name": "amsterdam, Amsterdam, IJsbaanpad", 
       "id": "57142580"
     }, 
     {
       "lat": "4.85729077275984", 
       "lon": "52.3346945047739", 
       "name": "amsterdam, Amsterdam, VU Medisch Centrum", 
       "id": "57142590"
     }, 
     {
       "lat": "4.85769920662217", 
       "lon": "52.3348940646888", 
       "name": "amsterdam, Amsterdam, VU Medisch Centrum", 
       "id": "57142600"
     }, 
     {
       "lat": "4.85738325448068", 
       "lon": "52.33063243219", 
       "name": "amsterdam, Amsterdam, Koenenkade", 
       "id": "57142610"
     }, 
     {
       "lat": "4.85756131398447", 
       "lon": "52.3316937903431", 
       "name": "amsterdam, Amsterdam, Koenenkade", 
       "id": "57142620"
     }, 
     {
       "lat": "4.85669420373807", 
       "lon": "52.344102048832", 
       "name": "amsterdam, Amsterdam, Stadionplein", 
       "id": "57142630"
     }, 
     {
       "lat": "4.85696209713029", 
       "lon": "52.3437886769886", 
       "name": "amsterdam, Amsterdam, Stadionplein", 
       "id": "57142640"
     }, 
     {
       "lat": "4.8572909199307", 
       "lon": "52.3383705138552", 
       "name": "amsterdam, Amsterdam, Stat. Amstelveenseweg", 
       "id": "57142870"
     }, 
     {
       "lat": "4.8575147576615", 
       "lon": "52.3380569432387", 
       "name": "amsterdam, Amsterdam, Stat. Amstelveenseweg", 
       "id": "57142880"
     }, 
     {
       "lat": "4.85866134747084", 
       "lon": "52.3391136414724", 
       "name": "amsterdam, Amsterdam, Stat. Amstelveenseweg", 
       "id": "57142881"
     }, 
     {
       "lat": "4.87944285670897", 
       "lon": "52.3259296685351", 
       "name": "amsterdam, Amsterdam, Kastelenstraat", 
       "id": "57142920"
     }, 
     {
       "lat": "4.87884466595059", 
       "lon": "52.334618296003", 
       "name": "amsterdam, Amsterdam, Hogewerf", 
       "id": "57142930"
     }, 
     {
       "lat": "4.86748490369535", 
       "lon": "52.3349374484122", 
       "name": "amsterdam, Amsterdam, De Boelelaan/VU", 
       "id": "57142940"
     }, 
     {
       "lat": "4.87940720527348", 
       "lon": "52.3341803098384", 
       "name": "amsterdam, Amsterdam, Hogewerf", 
       "id": "57142970"
     }, 
     {
       "lat": "4.87932817677335", 
       "lon": "52.3308275253457", 
       "name": "amsterdam, Amsterdam, Loowaard", 
       "id": "57142980"
     }, 
     {
       "lat": "4.87959079666146", 
       "lon": "52.3309544813504", 
       "name": "amsterdam, Amsterdam, Loowaard", 
       "id": "57142990"
     }, 
     {
       "lat": "4.87955249904147", 
       "lon": "52.326604224015", 
       "name": "amsterdam, Amsterdam, Kastelenstraat", 
       "id": "57143010"
     }, 
     {
       "lat": "4.86082268044519", 
       "lon": "52.3350338293466", 
       "name": "amsterdam, Amsterdam, VU Medisch Centrum", 
       "id": "57143070"
     }, 
     {
       "lat": "4.85683246259133", 
       "lon": "52.3374427172865", 
       "name": "amsterdam, Amsterdam, Stat. Amstelveenseweg", 
       "id": "57144010"
     }, 
     {
       "lat": "4.98073655093022", 
       "lon": "52.3334392869445", 
       "name": "diemen, Diemen, Vinkenbrug", 
       "id": "57152660"
     }, 
     {
       "lat": "4.98085622079678", 
       "lon": "52.3331880414148", 
       "name": "diemen, Diemen, Vinkenbrug", 
       "id": "57152690"
     }, 
     {
       "lat": "4.76696755180657", 
       "lon": "52.34118516883", 
       "name": "badhoevedorp, Badhoevedorp, Prins Mauritslaan", 
       "id": "57232010"
     }, 
     {
       "lat": "4.76759999963976", 
       "lon": "52.3410806277689", 
       "name": "badhoevedorp, Badhoevedorp, Prins Mauritslaan", 
       "id": "57232020"
     }, 
     {
       "lat": "4.77906514592082", 
       "lon": "52.332170229715", 
       "name": "badhoevedorp, Badhoevedorp, PA Verkuyllaan", 
       "id": "57232060"
     }, 
     {
       "lat": "4.7787548566381", 
       "lon": "52.3323304159253", 
       "name": "badhoevedorp, Badhoevedorp, PA Verkuyllaan", 
       "id": "57232070"
     }, 
     {
       "lat": "4.7802199410594", 
       "lon": "52.3356993976568", 
       "name": "badhoevedorp, Badhoevedorp, RK Kerk", 
       "id": "57232080"
     }, 
     {
       "lat": "4.77976660618914", 
       "lon": "52.3355892171259", 
       "name": "badhoevedorp, Badhoevedorp, RK Kerk", 
       "id": "57232090"
     }, 
     {
       "lat": "4.78160570920488", 
       "lon": "52.3373692497913", 
       "name": "badhoevedorp, Badhoevedorp, Reigerstraat", 
       "id": "57232110"
     }, 
     {
       "lat": "4.784964511719", 
       "lon": "52.3385458235081", 
       "name": "badhoevedorp, Badhoevedorp, Havikstraat", 
       "id": "57232120"
     }, 
     {
       "lat": "4.78490777341406", 
       "lon": "52.3384017292742", 
       "name": "badhoevedorp, Badhoevedorp, Havikstraat", 
       "id": "57232130"
     }, 
     {
       "lat": "4.78922212985553", 
       "lon": "52.3383696829043", 
       "name": "badhoevedorp, Badhoevedorp, Spechtstraat", 
       "id": "57232140"
     }, 
     {
       "lat": "4.78899962503925", 
       "lon": "52.3385483150646", 
       "name": "badhoevedorp, Badhoevedorp, Spechtstraat", 
       "id": "57232150"
     }, 
     {
       "lat": "4.79001506344155", 
       "lon": "52.3361447029725", 
       "name": "badhoevedorp, Badhoevedorp, Rijstvogelstraat", 
       "id": "57232170"
     }, 
     {
       "lat": "4.79013146836886", 
       "lon": "52.3362171931243", 
       "name": "badhoevedorp, Badhoevedorp, Rijstvogelstraat", 
       "id": "57232180"
     }, 
     {
       "lat": "4.81440129011417", 
       "lon": "52.3417837836892", 
       "name": "amsterdam, Amsterdam, Sloterweg 837", 
       "id": "57232190"
     }, 
     {
       "lat": "4.80746606678343", 
       "lon": "52.3413455603124", 
       "name": "amsterdam, Amsterdam, Sportpark Sloten", 
       "id": "57232200"
     }, 
     {
       "lat": "4.80676069452534", 
       "lon": "52.3414229930439", 
       "name": "amsterdam, Amsterdam, Sportpark Sloten", 
       "id": "57232210"
     }, 
     {
       "lat": "4.8009610864861", 
       "lon": "52.3416730271639", 
       "name": "amsterdam, Amsterdam, Ditlaar", 
       "id": "57232220"
     }, 
     {
       "lat": "4.80112261164733", 
       "lon": "52.3416648394035", 
       "name": "amsterdam, Amsterdam, Ditlaar", 
       "id": "57232230"
     }, 
     {
       "lat": "4.79763918179528", 
       "lon": "52.3431934423562", 
       "name": "amsterdam, Amsterdam, Osdorperweg", 
       "id": "57232240"
     }, 
     {
       "lat": "4.79734510842674", 
       "lon": "52.3432369160886", 
       "name": "amsterdam, Amsterdam, Osdorperweg", 
       "id": "57232250"
     }, 
     {
       "lat": "4.79363778532787", 
       "lon": "52.3417353879594", 
       "name": "amsterdam, Amsterdam, Langsom", 
       "id": "57232260"
     }, 
     {
       "lat": "4.78410230496825", 
       "lon": "52.328564918222", 
       "name": "badhoevedorp, Badhoevedorp, Schuilhoeve", 
       "id": "57232270"
     }, 
     {
       "lat": "4.81469580089358", 
       "lon": "52.3417043184969", 
       "name": "amsterdam, Amsterdam, Sloterweg 837", 
       "id": "57232320"
     }, 
     {
       "lat": "4.7719375681837", 
       "lon": "52.3383350020573", 
       "name": "badhoevedorp, Badhoevedorp, De Meerwende", 
       "id": "57232360"
     }, 
     {
       "lat": "4.7730660809345", 
       "lon": "52.338430742852", 
       "name": "badhoevedorp, Badhoevedorp, De Meerwende", 
       "id": "57232370"
     }, 
     {
       "lat": "4.77754935549032", 
       "lon": "52.3389212937777", 
       "name": "badhoevedorp, Badhoevedorp, Lorentzplein", 
       "id": "57232380"
     }, 
     {
       "lat": "4.7775954703755", 
       "lon": "52.338768737972", 
       "name": "badhoevedorp, Badhoevedorp, Lorentzplein", 
       "id": "57232390"
     }, 
     {
       "lat": "4.78075093629025", 
       "lon": "52.3376434953475", 
       "name": "badhoevedorp, Badhoevedorp, Reigerstraat", 
       "id": "57232400"
     }, 
     {
       "lat": "4.79290954998907", 
       "lon": "52.3369412175457", 
       "name": "badhoevedorp, Badhoevedorp, Uiverstraat", 
       "id": "57232410"
     }, 
     {
       "lat": "4.79261623559674", 
       "lon": "52.3369307562296", 
       "name": "badhoevedorp, Badhoevedorp, Uiverstraat", 
       "id": "57232420"
     }, 
     {
       "lat": "4.79309944195944", 
       "lon": "52.3391981179492", 
       "name": "badhoevedorp, Badhoevedorp, Nieuwe Meerdijk 69", 
       "id": "57232430"
     }, 
     {
       "lat": "4.79315680913737", 
       "lon": "52.3392972721219", 
       "name": "badhoevedorp, Badhoevedorp, Nieuwe Meerdijk 69", 
       "id": "57232440"
     }, 
     {
       "lat": "4.75076868609541", 
       "lon": "52.346204260313", 
       "name": "lijnden, Lijnden, Lijnden", 
       "id": "57232450"
     }, 
     {
       "lat": "4.79303774277484", 
       "lon": "52.341615534979", 
       "name": "amsterdam, Amsterdam, Langsom", 
       "id": "57232460"
     }, 
     {
       "lat": "4.77535128457703", 
       "lon": "52.3397727821924", 
       "name": "badhoevedorp, Badhoevedorp, Kamerlingh Onneslaan", 
       "id": "57232490"
     }, 
     {
       "lat": "4.77543795814362", 
       "lon": "52.3398720966095", 
       "name": "badhoevedorp, Badhoevedorp, Kamerlingh Onneslaan", 
       "id": "57232500"
     }, 
     {
       "lat": "4.82249643357992", 
       "lon": "52.342182201553", 
       "name": "amsterdam, Amsterdam, Sloterweg 700", 
       "id": "57232510"
     }, 
     {
       "lat": "4.82271779360384", 
       "lon": "52.3420843917372", 
       "name": "amsterdam, Amsterdam, Sloterweg 700", 
       "id": "57232520"
     }, 
     {
       "lat": "4.8249000477976", 
       "lon": "52.3424183418381", 
       "name": "amsterdam, Amsterdam, L. Armstrongstraat", 
       "id": "57232530"
     }, 
     {
       "lat": "4.82553112702291", 
       "lon": "52.3424123508924", 
       "name": "amsterdam, Amsterdam, L. Armstrongstraat", 
       "id": "57232540"
     }, 
     {
       "lat": "4.82750419090811", 
       "lon": "52.3442102716388", 
       "name": "amsterdam, Amsterdam, Henk Sneevlietweg", 
       "id": "57232550"
     }, 
     {
       "lat": "4.78300457590893", 
       "lon": "52.3294581034548", 
       "name": "badhoevedorp, Badhoevedorp, Schuilhoeve", 
       "id": "57232560"
     }, 
     {
       "lat": "4.8575242721885", 
       "lon": "52.3028157288594", 
       "name": "amstelveen, Amstelveen, Busstation", 
       "id": "57240010"
     }, 
     {
       "lat": "4.85873787538709", 
       "lon": "52.301859457338", 
       "name": "amstelveen, Amstelveen, Busstation", 
       "id": "57240018"
     }, 
     {
       "lat": "4.85848661929462", 
       "lon": "52.3020291036306", 
       "name": "amstelveen, Amstelveen, Busstation", 
       "id": "57240019"
     }, 
     {
       "lat": "4.85734920209977", 
       "lon": "52.3027430418392", 
       "name": "amstelveen, Amstelveen, Busstation", 
       "id": "57240021"
     }, 
     {
       "lat": "4.85725888118499", 
       "lon": "52.3029403699674", 
       "name": "amstelveen, Amstelveen, Busstation", 
       "id": "57240022"
     }, 
     {
       "lat": "4.85732073810465", 
       "lon": "52.3026710114791", 
       "name": "amstelveen, Amstelveen, Busstation", 
       "id": "57240023"
     }, 
     {
       "lat": "4.85713175866813", 
       "lon": "52.3025353468281", 
       "name": "amstelveen, Amstelveen, Busstation", 
       "id": "57240024"
     }, 
     {
       "lat": "4.85727922096116", 
       "lon": "52.3024641047994", 
       "name": "amstelveen, Amstelveen, Busstation", 
       "id": "57240025"
     }, 
     {
       "lat": "4.87093039085634", 
       "lon": "52.3035940358747", 
       "name": "amstelveen, Amstelveen, Oranjebaan", 
       "id": "57240050"
     }, 
     {
       "lat": "4.8730802365926", 
       "lon": "52.3027944945865", 
       "name": "amstelveen, Amstelveen, Oranjebaan", 
       "id": "57240060"
     }, 
     {
       "lat": "4.83263202846739", 
       "lon": "52.2826136984226", 
       "name": "amstelveen, Amstelveen, Sacharovlaan", 
       "id": "57240070"
     }, 
     {
       "lat": "4.83298952770971", 
       "lon": "52.2833254191933", 
       "name": "amstelveen, Amstelveen, Sacharovlaan", 
       "id": "57240080"
     }, 
     {
       "lat": "4.85841417295137", 
       "lon": "52.3019568768998", 
       "name": "amstelveen, Amstelveen, Busstation", 
       "id": "57240600"
     }, 
     {
       "lat": "4.85835446234534", 
       "lon": "52.3020464884689", 
       "name": "amstelveen, Amstelveen, Busstation", 
       "id": "57240610"
     }, 
     {
       "lat": "4.84221757876858", 
       "lon": "52.2872870371628", 
       "name": "amstelveen, Amstelveen, Bovenkerkerweg", 
       "id": "57242010"
     }, 
     {
       "lat": "4.84098301491721", 
       "lon": "52.2816009898554", 
       "name": "amstelveen, Amstelveen, Zagerij", 
       "id": "57242020"
     }, 
     {
       "lat": "4.84030247540833", 
       "lon": "52.2809327390412", 
       "name": "amstelveen, Amstelveen, Zagerij", 
       "id": "57242030"
     }, 
     {
       "lat": "4.83957790482118", 
       "lon": "52.2778914728865", 
       "name": "amstelveen, Amstelveen, Nesserlaan", 
       "id": "57242040"
     }, 
     {
       "lat": "4.84576191842984", 
       "lon": "52.2995268345335", 
       "name": "amstelveen, Amstelveen, Oakpark", 
       "id": "57242050"
     }, 
     {
       "lat": "4.86270410182887", 
       "lon": "52.3061733050245", 
       "name": "amstelveen, Amstelveen, Gr.v.Prinstererlaan", 
       "id": "57242060"
     }, 
     {
       "lat": "4.84593595611641", 
       "lon": "52.3032935463231", 
       "name": "amstelveen, Amstelveen, Dorpsstraat", 
       "id": "57242070"
     }, 
     {
       "lat": "4.86238324214083", 
       "lon": "52.306028076217", 
       "name": "amstelveen, Amstelveen, Gr.v.Prinstererlaan", 
       "id": "57242090"
     }, 
     {
       "lat": "4.87693918055745", 
       "lon": "52.3025325830875", 
       "name": "amstelveen, Amstelveen, Camera Obscuralaan", 
       "id": "57242110"
     }, 
     {
       "lat": "4.87710137482852", 
       "lon": "52.3024523921487", 
       "name": "amstelveen, Amstelveen, Camera Obscuralaan", 
       "id": "57242120"
     }, 
     {
       "lat": "4.87060486647925", 
       "lon": "52.3164631924486", 
       "name": "amstelveen, Amstelveen, Rembrandtweg", 
       "id": "57242130"
     }, 
     {
       "lat": "4.86317300250253", 
       "lon": "52.3111726228742", 
       "name": "amstelveen, Amstelveen, Zonnestein", 
       "id": "57242140"
     }, 
     {
       "lat": "4.8633815739642", 
       "lon": "52.31089492376", 
       "name": "amstelveen, Amstelveen, Zonnestein", 
       "id": "57242150"
     }, 
     {
       "lat": "4.87019811239894", 
       "lon": "52.3161288660279", 
       "name": "amstelveen, Amstelveen, Rembrandtweg", 
       "id": "57242190"
     }, 
     {
       "lat": "4.86888479731694", 
       "lon": "52.3218483598956", 
       "name": "amstelveen, Amstelveen, Kalfjeslaan/Beneluxb.", 
       "id": "57242200"
     }, 
     {
       "lat": "4.87495719993898", 
       "lon": "52.3167607410839", 
       "name": "amstelveen, Amstelveen, Saskia v.Uylenburgw.", 
       "id": "57242210"
     }, 
     {
       "lat": "4.86313000019837", 
       "lon": "52.3086019104995", 
       "name": "amstelveen, Amstelveen, Graaf Aelbrechtlaan", 
       "id": "57242220"
     }, 
     {
       "lat": "4.86331114204911", 
       "lon": "52.308162308727", 
       "name": "amstelveen, Amstelveen, Graaf Aelbrechtlaan", 
       "id": "57242230"
     }, 
     {
       "lat": "4.84561057255646", 
       "lon": "52.3035257411466", 
       "name": "amstelveen, Amstelveen, Dorpsstraat", 
       "id": "57242240"
     }, 
     {
       "lat": "4.84658576526393", 
       "lon": "52.3065231593415", 
       "name": "amstelveen, Amstelveen, KLM Hoofdkantoor", 
       "id": "57242250"
     }, 
     {
       "lat": "4.84677953807398", 
       "lon": "52.3062633970735", 
       "name": "amstelveen, Amstelveen, KLM Hoofdkantoor", 
       "id": "57242270"
     }, 
     {
       "lat": "4.83895627308019", 
       "lon": "52.2772055106392", 
       "name": "amstelveen, Amstelveen, Nesserlaan", 
       "id": "57242280"
     }, 
     {
       "lat": "4.84732612491775", 
       "lon": "52.3083420873325", 
       "name": "amstelveen, Amstelveen, Molenweg", 
       "id": "57242290"
     }, 
     {
       "lat": "4.84669957676721", 
       "lon": "52.3080156632004", 
       "name": "amstelveen, Amstelveen, Molenweg", 
       "id": "57242300"
     }, 
     {
       "lat": "4.85055391716899", 
       "lon": "52.3081860069677", 
       "name": "amstelveen, Amstelveen, Jan Benninghstraat", 
       "id": "57242470"
     }, 
     {
       "lat": "4.85631777777449", 
       "lon": "52.3068548526756", 
       "name": "amstelveen, Amstelveen, Heemraadschapslaan", 
       "id": "57242480"
     }, 
     {
       "lat": "4.85672498623599", 
       "lon": "52.3071353029799", 
       "name": "amstelveen, Amstelveen, Heemraadschapslaan", 
       "id": "57242490"
     }, 
     {
       "lat": "4.85946961500537", 
       "lon": "52.2834465777626", 
       "name": "amstelveen, Amstelveen, Logger", 
       "id": "57242520"
     }, 
     {
       "lat": "4.85996913698812", 
       "lon": "52.283340951657", 
       "name": "amstelveen, Amstelveen, Logger", 
       "id": "57242530"
     }, 
     {
       "lat": "4.86498551393379", 
       "lon": "52.282967747439", 
       "name": "amstelveen, Amstelveen, Punter", 
       "id": "57242540"
     }, 
     {
       "lat": "4.86491361570787", 
       "lon": "52.2828505873668", 
       "name": "amstelveen, Amstelveen, Punter", 
       "id": "57242550"
     }, 
     {
       "lat": "4.8664806770974", 
       "lon": "52.284187705854", 
       "name": "amstelveen, Amstelveen, Seine", 
       "id": "57242560"
     }, 
     {
       "lat": "4.86667171124889", 
       "lon": "52.2841436076232", 
       "name": "amstelveen, Amstelveen, Seine", 
       "id": "57242570"
     }, 
     {
       "lat": "4.86794846444188", 
       "lon": "52.2865040455717", 
       "name": "amstelveen, Amstelveen, Watercirkel", 
       "id": "57242580"
     }, 
     {
       "lat": "4.86855863867285", 
       "lon": "52.2869651051967", 
       "name": "amstelveen, Amstelveen, Watercirkel", 
       "id": "57242590"
     }, 
     {
       "lat": "4.86808417689548", 
       "lon": "52.2886886948347", 
       "name": "amstelveen, Amstelveen, Groenhof", 
       "id": "57242600"
     }, 
     {
       "lat": "4.86839601701974", 
       "lon": "52.2895978384381", 
       "name": "amstelveen, Amstelveen, Groenhof", 
       "id": "57242610"
     }, 
     {
       "lat": "4.85360751432988", 
       "lon": "52.2932260462992", 
       "name": "amstelveen, Amstelveen, van der Hooplaan", 
       "id": "57242680"
     }, 
     {
       "lat": "4.85297497703598", 
       "lon": "52.2934119357364", 
       "name": "amstelveen, Amstelveen, van der Hooplaan", 
       "id": "57242690"
     }, 
     {
       "lat": "4.84966595944419", 
       "lon": "52.2943137036138", 
       "name": "amstelveen, Amstelveen, Heilige Geestkerk", 
       "id": "57242700"
     }, 
     {
       "lat": "4.84961839980042", 
       "lon": "52.2946100872541", 
       "name": "amstelveen, Amstelveen, Heilige Geestkerk", 
       "id": "57242710"
     }, 
     {
       "lat": "4.84477724654647", 
       "lon": "52.3021288035181", 
       "name": "amstelveen, Amstelveen, Raadhuis", 
       "id": "57242740"
     }, 
     {
       "lat": "4.84490787384905", 
       "lon": "52.3022372569156", 
       "name": "amstelveen, Amstelveen, Raadhuis", 
       "id": "57242750"
     }, 
     {
       "lat": "4.84679505105747", 
       "lon": "52.3122224126247", 
       "name": "amstelveen, Amstelveen, Oude Karselaan", 
       "id": "57242760"
     }, 
     {
       "lat": "4.84701347668566", 
       "lon": "52.3123492401441", 
       "name": "amstelveen, Amstelveen, Oude Karselaan", 
       "id": "57242770"
     }, 
     {
       "lat": "4.84783794434239", 
       "lon": "52.3157054671508", 
       "name": "amstelveen, Amstelveen, Prins Bernhardlaan", 
       "id": "57242780"
     }, 
     {
       "lat": "4.849527663665", 
       "lon": "52.3154435242396", 
       "name": "amstelveen, Amstelveen, Prins Bernhardlaan", 
       "id": "57242790"
     }, 
     {
       "lat": "4.85132947748478", 
       "lon": "52.3156134812337", 
       "name": "amstelveen, Amstelveen, Julianapark", 
       "id": "57242800"
     }, 
     {
       "lat": "4.85354623959005", 
       "lon": "52.3154257699882", 
       "name": "amstelveen, Amstelveen, Julianapark", 
       "id": "57242810"
     }, 
     {
       "lat": "4.85682277761805", 
       "lon": "52.3161415568139", 
       "name": "amstelveen, Amstelveen, Graaf Florislaan", 
       "id": "57242820"
     }, 
     {
       "lat": "4.85715942925285", 
       "lon": "52.3161969926996", 
       "name": "amstelveen, Amstelveen, Graaf Florislaan", 
       "id": "57242830"
     }, 
     {
       "lat": "4.8573627165543", 
       "lon": "52.3225163449327", 
       "name": "amstelveen, Amstelveen, Kalfjesl./Amstelv.wg", 
       "id": "57242840"
     }, 
     {
       "lat": "4.87028829984361", 
       "lon": "52.2919879104265", 
       "name": "amstelveen, Amstelveen, In de Wolken", 
       "id": "57242850"
     }, 
     {
       "lat": "4.8696335450734", 
       "lon": "52.2915716046513", 
       "name": "amstelveen, Amstelveen, In de Wolken", 
       "id": "57242860"
     }, 
     {
       "lat": "4.87199054631545", 
       "lon": "52.2943501590494", 
       "name": "amstelveen, Amstelveen, Ziekenhuis", 
       "id": "57242870"
     }, 
     {
       "lat": "4.87184157177593", 
       "lon": "52.2945562306889", 
       "name": "amstelveen, Amstelveen, Ziekenhuis", 
       "id": "57242880"
     }, 
     {
       "lat": "4.86098843834208", 
       "lon": "52.2962790440366", 
       "name": "amstelveen, Amstelveen, Johannes Calvijnlaan", 
       "id": "57242910"
     }, 
     {
       "lat": "4.86199955302489", 
       "lon": "52.2963105024334", 
       "name": "amstelveen, Amstelveen, Johannes Calvijnlaan", 
       "id": "57242920"
     }, 
     {
       "lat": "4.85762598010099", 
       "lon": "52.2967403912239", 
       "name": "amstelveen, Amstelveen, Ingenieur Romplaan", 
       "id": "57242930"
     }, 
     {
       "lat": "4.85771510918692", 
       "lon": "52.2966419238046", 
       "name": "amstelveen, Amstelveen, Ingenieur Romplaan", 
       "id": "57242940"
     }, 
     {
       "lat": "4.85520390181337", 
       "lon": "52.2982394814707", 
       "name": "amstelveen, Amstelveen, Hueseplein", 
       "id": "57242950"
     }, 
     {
       "lat": "4.85475732851773", 
       "lon": "52.2975813576133", 
       "name": "amstelveen, Amstelveen, Hueseplein", 
       "id": "57242960"
     }, 
     {
       "lat": "4.87319341737009", 
       "lon": "52.2930072144746", 
       "name": "amstelveen, Amstelveen, Ziekenhuis (lvHM)", 
       "id": "57242990"
     }, 
     {
       "lat": "4.87279413222582", 
       "lon": "52.2933110655345", 
       "name": "amstelveen, Amstelveen, Ziekenhuis (lvHM)", 
       "id": "57243000"
     }, 
     {
       "lat": "4.8684001667403", 
       "lon": "52.2967791601126", 
       "name": "amstelveen, Amstelveen, Ouderkerkerlaan", 
       "id": "57243010"
     }, 
     {
       "lat": "4.87616847504167", 
       "lon": "52.3019809970333", 
       "name": "amstelveen, Amstelveen, Bankrashof", 
       "id": "57243020"
     }, 
     {
       "lat": "4.8758417078765", 
       "lon": "52.302348086272", 
       "name": "amstelveen, Amstelveen, Bankrashof", 
       "id": "57243030"
     }, 
     {
       "lat": "4.86830968954596", 
       "lon": "52.3020186817867", 
       "name": "amstelveen, Amstelveen, Gas en Water", 
       "id": "57243040"
     }, 
     {
       "lat": "4.86851461992734", 
       "lon": "52.302046544256", 
       "name": "amstelveen, Amstelveen, Gas en Water", 
       "id": "57243050"
     }, 
     {
       "lat": "4.86334777523702", 
       "lon": "52.3013227190744", 
       "name": "amstelveen, Amstelveen, Binnenhof", 
       "id": "57243060"
     }, 
     {
       "lat": "4.86315528641107", 
       "lon": "52.3014836476748", 
       "name": "amstelveen, Amstelveen, Binnenhof", 
       "id": "57243070"
     }, 
     {
       "lat": "4.87361308912411", 
       "lon": "52.3163145100983", 
       "name": "amstelveen, Amstelveen, Saskia v.Uylenburgw.", 
       "id": "57243080"
     }, 
     {
       "lat": "4.84469496237085", 
       "lon": "52.2956571601269", 
       "name": "amstelveen, Amstelveen, 't Huis a/d Poel", 
       "id": "57243090"
     }, 
     {
       "lat": "4.84458807667777", 
       "lon": "52.2960071968502", 
       "name": "amstelveen, Amstelveen, 't Huis a/d Poel", 
       "id": "57243100"
     }, 
     {
       "lat": "4.84287907761578", 
       "lon": "52.2883236915387", 
       "name": "amstelveen, Amstelveen, Bovenkerkerweg", 
       "id": "57243110"
     }, 
     {
       "lat": "4.85332234297651", 
       "lon": "52.2864568860007", 
       "name": "amstelveen, Amstelveen, Startbaan", 
       "id": "57243120"
     }, 
     {
       "lat": "4.8539747140648", 
       "lon": "52.2870530301636", 
       "name": "amstelveen, Amstelveen, Startbaan", 
       "id": "57243130"
     }, 
     {
       "lat": "4.85118609083431", 
       "lon": "52.2837328785996", 
       "name": "amstelveen, Amstelveen, Grote Beer", 
       "id": "57243140"
     }, 
     {
       "lat": "4.85123124519573", 
       "lon": "52.283634216495", 
       "name": "amstelveen, Amstelveen, Grote Beer", 
       "id": "57243150"
     }, 
     {
       "lat": "4.84499335524194", 
       "lon": "52.2832103073429", 
       "name": "amstelveen, Amstelveen, Poortwachter", 
       "id": "57243160"
     }, 
     {
       "lat": "4.84477387244514", 
       "lon": "52.2831823369174", 
       "name": "amstelveen, Amstelveen, Poortwachter", 
       "id": "57243170"
     }, 
     {
       "lat": "4.8433398894174", 
       "lon": "52.2913906810108", 
       "name": "amstelveen, Amstelveen, Handweg", 
       "id": "57243180"
     }, 
     {
       "lat": "4.85688027652048", 
       "lon": "52.3113243345374", 
       "name": "amstelveen, Amstelveen, Kruiskerk", 
       "id": "57243210"
     }, 
     {
       "lat": "4.85644198456902", 
       "lon": "52.3111875510999", 
       "name": "amstelveen, Amstelveen, Kruiskerk", 
       "id": "57243220"
     }, 
     {
       "lat": "4.85690496061116", 
       "lon": "52.3129422561678", 
       "name": "amstelveen, Amstelveen, Dijkgravenlaan", 
       "id": "57243230"
     }, 
     {
       "lat": "4.85652101469253", 
       "lon": "52.3131652302376", 
       "name": "amstelveen, Amstelveen, Dijkgravenlaan", 
       "id": "57243240"
     }, 
     {
       "lat": "4.85373400276747", 
       "lon": "52.298565411025", 
       "name": "amstelveen, Amstelveen, Keizer Karelplein", 
       "id": "57243250"
     }, 
     {
       "lat": "4.85383435253468", 
       "lon": "52.2987546087905", 
       "name": "amstelveen, Amstelveen, Keizer Karelplein", 
       "id": "57243260"
     }, 
     {
       "lat": "4.84383196010929", 
       "lon": "52.2919052524749", 
       "name": "amstelveen, Amstelveen, Handweg", 
       "id": "57243270"
     }, 
     {
       "lat": "4.85439231905418", 
       "lon": "52.2913421313442", 
       "name": "amstelveen, Amstelveen, Sportlaan", 
       "id": "57243280"
     }, 
     {
       "lat": "4.85471433834118", 
       "lon": "52.2913795333721", 
       "name": "amstelveen, Amstelveen, Sportlaan", 
       "id": "57243290"
     }, 
     {
       "lat": "4.82546332151827", 
       "lon": "52.2816541009323", 
       "name": "amstelveen, Amstelveen, Westwijkplein", 
       "id": "57243300"
     }, 
     {
       "lat": "4.8256240567255", 
       "lon": "52.2816908161679", 
       "name": "amstelveen, Amstelveen, Westwijkplein", 
       "id": "57243310"
     }, 
     {
       "lat": "4.85461663157677", 
       "lon": "52.2946416912949", 
       "name": "amstelveen, Amstelveen, Doctor Plesmansingel", 
       "id": "57243320"
     }, 
     {
       "lat": "4.85479597051156", 
       "lon": "52.2943548869913", 
       "name": "amstelveen, Amstelveen, Doctor Plesmansingel", 
       "id": "57243330"
     }, 
     {
       "lat": "4.88151086957876", 
       "lon": "52.3079179561649", 
       "name": "amstelveen, Amstelveen, Lien Gisolflaan", 
       "id": "57243350"
     }, 
     {
       "lat": "4.8816329736138", 
       "lon": "52.3074960500714", 
       "name": "amstelveen, Amstelveen, Lien Gisolflaan", 
       "id": "57243370"
     }, 
     {
       "lat": "4.81990813622229", 
       "lon": "52.2817444189807", 
       "name": "amstelveen, Amstelveen, Boschplaat", 
       "id": "57243380"
     }, 
     {
       "lat": "4.8216601409361", 
       "lon": "52.281105682769", 
       "name": "amstelveen, Amstelveen, Boschplaat", 
       "id": "57243390"
     }, 
     {
       "lat": "4.86734422003178", 
       "lon": "52.2968194623092", 
       "name": "amstelveen, Amstelveen, Ouderkerkerlaan", 
       "id": "57243400"
     }, 
     {
       "lat": "4.84735217171928", 
       "lon": "52.2965411439675", 
       "name": "amstelveen, Amstelveen, Lindenlaan", 
       "id": "57243410"
     }, 
     {
       "lat": "4.8471166528545", 
       "lon": "52.2966209594342", 
       "name": "amstelveen, Amstelveen, Lindenlaan", 
       "id": "57243420"
     }, 
     {
       "lat": "4.85055066937347", 
       "lon": "52.2975263916897", 
       "name": "amstelveen, Amstelveen, Icaruslaan", 
       "id": "57243430"
     }, 
     {
       "lat": "4.85043209638201", 
       "lon": "52.297633707976", 
       "name": "amstelveen, Amstelveen, Icaruslaan", 
       "id": "57243440"
     }, 
     {
       "lat": "4.84652282159397", 
       "lon": "52.2912075441014", 
       "name": "amstelveen, Amstelveen, Wimbledonpark", 
       "id": "57243450"
     }, 
     {
       "lat": "4.84886996980554", 
       "lon": "52.2910474832001", 
       "name": "amstelveen, Amstelveen, Wimbledonpark", 
       "id": "57243460"
     }, 
     {
       "lat": "4.88134643803948", 
       "lon": "52.3172106618384", 
       "name": "amstelveen, Amstelveen, Gan Hasjalom", 
       "id": "57243470"
     }, 
     {
       "lat": "4.88150734821915", 
       "lon": "52.3172473010461", 
       "name": "amstelveen, Amstelveen, Gan Hasjalom", 
       "id": "57243480"
     }, 
     {
       "lat": "4.88127076829091", 
       "lon": "52.3135522963413", 
       "name": "amstelveen, Amstelveen, R. Blokland Paterln.", 
       "id": "57243490"
     }, 
     {
       "lat": "4.88135691174368", 
       "lon": "52.3137144455166", 
       "name": "amstelveen, Amstelveen, R. Blokland Paterln.", 
       "id": "57243500"
     }, 
     {
       "lat": "4.88132547228143", 
       "lon": "52.3113235501799", 
       "name": "amstelveen, Amstelveen, Machineweg", 
       "id": "57243510"
     }, 
     {
       "lat": "4.88142555907882", 
       "lon": "52.3115486737889", 
       "name": "amstelveen, Amstelveen, Machineweg", 
       "id": "57243520"
     }, 
     {
       "lat": "4.84571082357123", 
       "lon": "52.3001108119635", 
       "name": "amstelveen, Amstelveen, Oakpark", 
       "id": "57243540"
     }, 
     {
       "lat": "4.84161930889472", 
       "lon": "52.2918501249455", 
       "name": "amstelveen, Amstelveen, Maalderij", 
       "id": "57243550"
     }, 
     {
       "lat": "4.84176477586297", 
       "lon": "52.2919406748511", 
       "name": "amstelveen, Amstelveen, Maalderij", 
       "id": "57243560"
     }, 
     {
       "lat": "4.836783600194", 
       "lon": "52.2929242368854", 
       "name": "bovenkerk, Bovenkerk, Pastoor Brouwerslaan", 
       "id": "57243570"
     }, 
     {
       "lat": "4.83639994957284", 
       "lon": "52.2931291718472", 
       "name": "bovenkerk, Bovenkerk, Pastoor Brouwerslaan", 
       "id": "57243580"
     }, 
     {
       "lat": "4.83182618096419", 
       "lon": "52.2931617065137", 
       "name": "bovenkerk, Bovenkerk, Zwarte Pad", 
       "id": "57243590"
     }, 
     {
       "lat": "4.83148894923602", 
       "lon": "52.2931691100804", 
       "name": "bovenkerk, Bovenkerk, Zwarte Pad", 
       "id": "57243600"
     }, 
     {
       "lat": "4.82658674250925", 
       "lon": "52.2913483922289", 
       "name": "bovenkerk, Bovenkerk, Schinkeldijkje", 
       "id": "57243610"
     }, 
     {
       "lat": "4.88154161060334", 
       "lon": "52.3039274891998", 
       "name": "amstelveen, Amstelveen, Escapade", 
       "id": "57243640"
     }, 
     {
       "lat": "4.8323397210229", 
       "lon": "52.2755028890977", 
       "name": "amstelveen, Amstelveen, Hammarskjoldsingel", 
       "id": "57243650"
     }, 
     {
       "lat": "4.85575873382137", 
       "lon": "52.2800325331952", 
       "name": "amstelveen, Amstelveen, Praam", 
       "id": "57243680"
     }, 
     {
       "lat": "4.85536406778031", 
       "lon": "52.2799498674291", 
       "name": "amstelveen, Amstelveen, Praam", 
       "id": "57243690"
     }, 
     {
       "lat": "4.85128228969634", 
       "lon": "52.280614515554", 
       "name": "amstelveen, Amstelveen, Middenhoven/Brink", 
       "id": "57243700"
     }, 
     {
       "lat": "4.85220814836691", 
       "lon": "52.2803940113619", 
       "name": "amstelveen, Amstelveen, Middenhoven/Brink", 
       "id": "57243710"
     }, 
     {
       "lat": "4.84204689297536", 
       "lon": "52.288059208898", 
       "name": "amstelveen, Amstelveen, Gieterij", 
       "id": "57243720"
     }, 
     {
       "lat": "4.84623576995694", 
       "lon": "52.2798635124688", 
       "name": "amstelveen, Amstelveen, De Eindhoeve", 
       "id": "57243730"
     }, 
     {
       "lat": "4.83515217335931", 
       "lon": "52.2897349192947", 
       "name": "bovenkerk, Bovenkerk, Zetterij", 
       "id": "57243740"
     }, 
     {
       "lat": "4.84611756184049", 
       "lon": "52.2799438626372", 
       "name": "amstelveen, Amstelveen, De Eindhoeve", 
       "id": "57243760"
     }, 
     {
       "lat": "4.84147342028663", 
       "lon": "52.2810460046077", 
       "name": "amstelveen, Amstelveen, Zagerij", 
       "id": "57243770"
     }, 
     {
       "lat": "4.84183733052462", 
       "lon": "52.2812454176451", 
       "name": "amstelveen, Amstelveen, Zagerij", 
       "id": "57243820"
     }, 
     {
       "lat": "4.88163841059032", 
       "lon": "52.3044402097266", 
       "name": "amstelveen, Amstelveen, Escapade", 
       "id": "57243830"
     }, 
     {
       "lat": "4.84689523310307", 
       "lon": "52.3088074880648", 
       "name": "amstelveen, Amstelveen, Molenweg", 
       "id": "57243850"
     }, 
     {
       "lat": "4.83245401918316", 
       "lon": "52.2757371113527", 
       "name": "amstelveen, Amstelveen, Hammarskjoldsingel", 
       "id": "57243860"
     }, 
     {
       "lat": "4.82907850055727", 
       "lon": "52.2773390484482", 
       "name": "amstelveen, Amstelveen, B.v.Suttnerlaan", 
       "id": "57243870"
     }, 
     {
       "lat": "4.82775381662798", 
       "lon": "52.2778091467549", 
       "name": "amstelveen, Amstelveen, B.v.Suttnerlaan", 
       "id": "57243880"
     }, 
     {
       "lat": "4.82805644280597", 
       "lon": "52.2852076284221", 
       "name": "amstelveen, Amstelveen, Noorddammerweg", 
       "id": "57243890"
     }, 
     {
       "lat": "4.83148710351209", 
       "lon": "52.2897986423634", 
       "name": "bovenkerk, Bovenkerk, Noorddammerweg", 
       "id": "57243910"
     }, 
     {
       "lat": "4.86349431161212", 
       "lon": "52.3137715298969", 
       "name": "amstelveen, Amstelveen, Laan Walcheren", 
       "id": "57244630"
     }, 
     {
       "lat": "4.86351463632836", 
       "lon": "52.3145355855143", 
       "name": "amstelveen, Amstelveen, Laan Walcheren", 
       "id": "57244640"
     }, 
     {
       "lat": "4.94794713143781", 
       "lon": "52.3036534756199", 
       "name": "amsterdam-zo, Amsterdam-ZO, Laarderhoogtweg", 
       "id": "57250320"
     }, 
     {
       "lat": "4.9512422249728", 
       "lon": "52.321973780533", 
       "name": "amsterdam-zo, Amsterdam-ZO, Dennenrode", 
       "id": "57250410"
     }, 
     {
       "lat": "4.94751365011463", 
       "lon": "52.3119026596533", 
       "name": "amsterdam-zo, Amsterdam-ZO, Bijlmer ArenA", 
       "id": "57250500"
     }, 
     {
       "lat": "4.94732684670014", 
       "lon": "52.3115154903461", 
       "name": "amsterdam-zo, Amsterdam-ZO, Bijlmer ArenA", 
       "id": "57250530"
     }, 
     {
       "lat": "4.97089669111073", 
       "lon": "52.3251183804853", 
       "name": "amsterdam-zo, Amsterdam-ZO, Geldershoofd", 
       "id": "57252160"
     }, 
     {
       "lat": "4.97320418902861", 
       "lon": "52.3230592935856", 
       "name": "amsterdam-zo, Amsterdam-ZO, Ganzenhoefstation", 
       "id": "57252180"
     }, 
     {
       "lat": "4.97633787738201", 
       "lon": "52.3236274573489", 
       "name": "amsterdam-zo, Amsterdam-ZO, Grubbehoeve", 
       "id": "57252220"
     }, 
     {
       "lat": "4.98086168821664", 
       "lon": "52.3229689982414", 
       "name": "amsterdam-zo, Amsterdam-ZO, Geerdinkhof", 
       "id": "57252240"
     }, 
     {
       "lat": "4.98406297309483", 
       "lon": "52.3193309215311", 
       "name": "amsterdam-zo, Amsterdam-ZO, Koornhorst", 
       "id": "57252280"
     }, 
     {
       "lat": "4.98182593482912", 
       "lon": "52.3169594975482", 
       "name": "amsterdam-zo, Amsterdam-ZO, Kraaienneststation", 
       "id": "57252320"
     }, 
     {
       "lat": "4.95945769415948", 
       "lon": "52.2974311650768", 
       "name": "amsterdam-zo, Amsterdam-ZO, Station Holendrecht", 
       "id": "57252470"
     }, 
     {
       "lat": "4.98494244284101", 
       "lon": "52.3112898681301", 
       "name": "amsterdam-zo, Amsterdam-ZO, Gaasperplasstation", 
       "id": "57252550"
     }, 
     {
       "lat": "4.94119816310178", 
       "lon": "52.3084996072048", 
       "name": "amsterdam-zo, Amsterdam-ZO, Holterbergweg", 
       "id": "57252670"
     }, 
     {
       "lat": "4.93972638085005", 
       "lon": "52.3090423043195", 
       "name": "amsterdam-zo, Amsterdam-ZO, Holterbergweg", 
       "id": "57252680"
     }, 
     {
       "lat": "4.95133002112506", 
       "lon": "52.31601521104", 
       "name": "amsterdam-zo, Amsterdam-ZO, Frissenstein", 
       "id": "57252720"
     }, 
     {
       "lat": "4.94837899821919", 
       "lon": "52.3193118032797", 
       "name": "amsterdam-zo, Amsterdam-ZO, Dolingadreef", 
       "id": "57252740"
     }, 
     {
       "lat": "4.95111930601095", 
       "lon": "52.3150707177838", 
       "name": "amsterdam-zo, Amsterdam-ZO, Bijlmerplein", 
       "id": "57252800"
     }, 
     {
       "lat": "4.93068745630242", 
       "lon": "52.309654887355", 
       "name": "amsterdam-zo, Amsterdam-ZO, Ventweg", 
       "id": "57252810"
     }, 
     {
       "lat": "4.93039456607814", 
       "lon": "52.3096178054495", 
       "name": "amsterdam-zo, Amsterdam-ZO, Ventweg", 
       "id": "57252820"
     }, 
     {
       "lat": "4.93636165484228", 
       "lon": "52.3111596356904", 
       "name": "amsterdam-zo, Amsterdam-ZO, de Entree", 
       "id": "57252840"
     }, 
     {
       "lat": "4.93681667862652", 
       "lon": "52.3111164300324", 
       "name": "amsterdam-zo, Amsterdam-ZO, de Entree", 
       "id": "57252850"
     }, 
     {
       "lat": "4.96241171275569", 
       "lon": "52.3257982555897", 
       "name": "amsterdam-zo, Amsterdam-ZO, Eeftink", 
       "id": "57252860"
     }, 
     {
       "lat": "4.96451720225026", 
       "lon": "52.3265158281565", 
       "name": "amsterdam-zo, Amsterdam-ZO, Egeldonk", 
       "id": "57252920"
     }, 
     {
       "lat": "4.94906409750838", 
       "lon": "52.3212287376421", 
       "name": "amsterdam-zo, Amsterdam-ZO, Daalwijk", 
       "id": "57253010"
     }, 
     {
       "lat": "4.94418202312176", 
       "lon": "52.3077738208886", 
       "name": "amsterdam-zo, Amsterdam-ZO, Gebouw Atlas", 
       "id": "57253030"
     }, 
     {
       "lat": "4.95511454201749", 
       "lon": "52.2963278527168", 
       "name": "amsterdam-zo, Amsterdam-ZO, Paasheuvelweg", 
       "id": "57253480"
     }, 
     {
       "lat": "4.95574067652449", 
       "lon": "52.2967615534456", 
       "name": "amsterdam-zo, Amsterdam-ZO, Paasheuvelweg", 
       "id": "57253490"
     }, 
     {
       "lat": "4.95403461352891", 
       "lon": "52.3229097765055", 
       "name": "amsterdam-zo, Amsterdam-ZO, Develstein", 
       "id": "57254020"
     }, 
     {
       "lat": "4.95970697393368", 
       "lon": "52.324862775543", 
       "name": "amsterdam-zo, Amsterdam-ZO, Echtenstein", 
       "id": "57254040"
     }, 
     {
       "lat": "4.73666416028014", 
       "lon": "52.2941954279655", 
       "name": "ONBEKEND, Schiphol Zuid, Valkweg", 
       "id": "57330050"
     }, 
     {
       "lat": "4.73488768279748", 
       "lon": "52.2933857131339", 
       "name": "ONBEKEND, Schiphol Zuid, Valkweg", 
       "id": "57330060"
     }, 
     {
       "lat": "4.74406560486235", 
       "lon": "52.3003567050147", 
       "name": "ONBEKEND, Schiphol Zuid, Uiverweg", 
       "id": "57330070"
     }, 
     {
       "lat": "4.74346677623855", 
       "lon": "52.3002006518775", 
       "name": "ONBEKEND, Schiphol Zuid, Uiverweg", 
       "id": "57330080"
     }, 
     {
       "lat": "4.74991032659631", 
       "lon": "52.3027431844711", 
       "name": "schiphol centrum, Schiphol Centrum, Schipholgebouw", 
       "id": "57330090"
     }, 
     {
       "lat": "4.74948375799992", 
       "lon": "52.3028397522619", 
       "name": "schiphol centrum, Schiphol Centrum, Schipholgebouw", 
       "id": "57330100"
     }, 
     {
       "lat": "4.75387335443096", 
       "lon": "52.3044901553978", 
       "name": "schiphol centrum, Schiphol Centrum, P12/Vrachtgebouw", 
       "id": "57330130"
     }, 
     {
       "lat": "4.76122584161543", 
       "lon": "52.3092120030386", 
       "name": "schiphol centrum, Schiphol Centrum, Plaza/NS", 
       "id": "57330221"
     }, 
     {
       "lat": "4.76136134836265", 
       "lon": "52.308961058648", 
       "name": "schiphol centrum, Schiphol Centrum, Plaza/NS", 
       "id": "57330224"
     }, 
     {
       "lat": "4.76103434249699", 
       "lon": "52.3092739047469", 
       "name": "schiphol centrum, Schiphol Centrum, Plaza/NS", 
       "id": "57330226"
     }, 
     {
       "lat": "4.78786547229988", 
       "lon": "52.3225621734166", 
       "name": "ONBEKEND, Schiphol Noord, Elzenhof", 
       "id": "57330250"
     }, 
     {
       "lat": "4.78534232023244", 
       "lon": "52.3236638595762", 
       "name": "ONBEKEND, Schiphol Noord, Elzenhof", 
       "id": "57330260"
     }, 
     {
       "lat": "4.79570535792071", 
       "lon": "52.3209209008663", 
       "name": "ONBEKEND, Schiphol Noord, Loevesteinse Dwarsw.", 
       "id": "57330270"
     }, 
     {
       "lat": "4.73403901516994", 
       "lon": "52.2912868336865", 
       "name": "ONBEKEND, Schiphol Zuid, P30 Parkeerterrein", 
       "id": "57330300"
     }, 
     {
       "lat": "4.73372977492052", 
       "lon": "52.2913839926188", 
       "name": "ONBEKEND, Schiphol Zuid, P30 Parkeerterrein", 
       "id": "57330310"
     }, 
     {
       "lat": "4.77479258883703", 
       "lon": "52.3217672041671", 
       "name": "ONBEKEND, Schiphol Noord, P40 Parkeerterrein", 
       "id": "57330400"
     }, 
     {
       "lat": "4.77478899554447", 
       "lon": "52.3220278340213", 
       "name": "ONBEKEND, Schiphol Noord, P40 Parkeerterrein", 
       "id": "57330410"
     }, 
     {
       "lat": "4.76359442019829", 
       "lon": "52.307615679182", 
       "name": "schiphol centrum, Schiphol Centrum, Skyport", 
       "id": "57330430"
     }, 
     {
       "lat": "4.76256137791109", 
       "lon": "52.3070439893956", 
       "name": "schiphol centrum, Schiphol Centrum, Skyport", 
       "id": "57330440"
     }, 
     {
       "lat": "4.75982297812122", 
       "lon": "52.3057532111217", 
       "name": "schiphol centrum, Schiphol Centrum, Martinair", 
       "id": "57330470"
     }, 
     {
       "lat": "4.75859422044251", 
       "lon": "52.3055489524182", 
       "name": "schiphol centrum, Schiphol Centrum, Martinair", 
       "id": "57330480"
     }, 
     {
       "lat": "4.75441644885682", 
       "lon": "52.3044481228442", 
       "name": "schiphol centrum, Schiphol Centrum, P12/Vrachtgebouw", 
       "id": "57330490"
     }, 
     {
       "lat": "4.76229014567029", 
       "lon": "52.3190324184941", 
       "name": "schiphol centrum, Schiphol Centrum, Sleepterrein", 
       "id": "57330530"
     }, 
     {
       "lat": "4.76192286934957", 
       "lon": "52.3190754171898", 
       "name": "schiphol centrum, Schiphol Centrum, Sleepterrein", 
       "id": "57330540"
     }, 
     {
       "lat": "4.75158906939035", 
       "lon": "52.3032555428261", 
       "name": "schiphol, Schiphol, Handelskade", 
       "id": "57330600"
     }, 
     {
       "lat": "4.75077232727702", 
       "lon": "52.3029545487898", 
       "name": "schiphol, Schiphol, Handelskade", 
       "id": "57330610"
     }, 
     {
       "lat": "4.76167166309256", 
       "lon": "52.3087919299353", 
       "name": "schiphol centrum, Schiphol Centrum, Plaza/NS", 
       "id": "57330620"
     }, 
     {
       "lat": "4.76171818027781", 
       "lon": "52.3086124177357", 
       "name": "schiphol centrum, Schiphol Centrum, Plaza/NS", 
       "id": "57330630"
     }, 
     {
       "lat": "4.79963689034345", 
       "lon": "52.3230885914418", 
       "name": "ONBEKEND, Schiphol Noord", 
       "id": "57330640"
     }, 
     {
       "lat": "4.78624043241918", 
       "lon": "52.3234167649137", 
       "name": "schiphol, Schiphol, Elzenhof", 
       "id": "57330650"
     }, 
     {
       "lat": "4.78630287048735", 
       "lon": "52.3231384581913", 
       "name": "schiphol, Schiphol, Elzenhof", 
       "id": "57330700"
     }, 
     {
       "lat": "4.80010255753781", 
       "lon": "52.3233695268512", 
       "name": "ONBEKEND, Schiphol Noord", 
       "id": "57330720"
     }, 
     {
       "lat": "4.75011899775083", 
       "lon": "52.3045508822708", 
       "name": "schiphol centrum, Schiphol Centrum, Aviodome", 
       "id": "57332030"
     }, 
     {
       "lat": "4.75060422507927", 
       "lon": "52.3044546279217", 
       "name": "schiphol centrum, Schiphol Centrum, Aviodome", 
       "id": "57332039"
     }, 
     {
       "lat": "4.76150822572523", 
       "lon": "52.3089438599177", 
       "name": "schiphol centrum, Schiphol Centrum, Plaza/NS", 
       "id": "57332103"
     }, 
     {
       "lat": "4.76106252781288", 
       "lon": "52.3093549451481", 
       "name": "schiphol centrum, Schiphol Centrum, Plaza/NS", 
       "id": "57332105"
     }, 
     {
       "lat": "4.76107731700417", 
       "lon": "52.3093460355292", 
       "name": "schiphol centrum, Schiphol Centrum, Plaza/NS", 
       "id": "57332107"
     }, 
     {
       "lat": "4.76171818027781", 
       "lon": "52.3086124177357", 
       "name": "schiphol centrum, Schiphol Centrum, Plaza/NS", 
       "id": "57332108"
     }, 
     {
       "lat": "4.73767350866226", 
       "lon": "52.2953424466137", 
       "name": "ONBEKEND, Schiphol Zuid, Toekanweg", 
       "id": "57332180"
     }, 
     {
       "lat": "4.73945063898003", 
       "lon": "52.2961161705651", 
       "name": "ONBEKEND, Schiphol Zuid, Toekanweg", 
       "id": "57332290"
     }, 
     {
       "lat": "4.72765799936671", 
       "lon": "52.2876652128627", 
       "name": "rozenburg, Rozenburg, Kruisweg", 
       "id": "57332315"
     }, 
     {
       "lat": "4.72741779396551", 
       "lon": "52.2870616784639", 
       "name": "rozenburg, Rozenburg, Kruisweg", 
       "id": "57332320"
     }, 
     {
       "lat": "4.72614609627237", 
       "lon": "52.2878185528723", 
       "name": "rozenburg, Rozenburg, Kruisweg", 
       "id": "57332375"
     }, 
     {
       "lat": "4.79619245970581", 
       "lon": "52.3206896508743", 
       "name": "ONBEKEND, Schiphol Noord, Loevesteinse Dwarsw.", 
       "id": "57340170"
     }, 
     {
       "lat": "4.81049812597128", 
       "lon": "52.3135250266282", 
       "name": "schiphol oost, Schiphol Oost, Gebouw 70", 
       "id": "57340270"
     }, 
     {
       "lat": "4.81005668714942", 
       "lon": "52.313639715871", 
       "name": "schiphol oost, Schiphol Oost, Gebouw 70", 
       "id": "57340280"
     }, 
     {
       "lat": "4.80927338708991", 
       "lon": "52.3084678649546", 
       "name": "schiphol oost, Schiphol Oost, Stationsplein", 
       "id": "57340334"
     }, 
     {
       "lat": "4.81235193148896", 
       "lon": "52.310792750442", 
       "name": "schiphol oost, Schiphol Oost, Gebouw 133", 
       "id": "57340337"
     }, 
     {
       "lat": "4.80681857108409", 
       "lon": "52.3066852324471", 
       "name": "schiphol oost, Schiphol Oost, REPA", 
       "id": "57340360"
     }, 
     {
       "lat": "4.80709808335034", 
       "lon": "52.3066147006578", 
       "name": "schiphol oost, Schiphol Oost, REPA", 
       "id": "57340370"
     }, 
     {
       "lat": "4.79700028366216", 
       "lon": "52.3018371109818", 
       "name": "schiphol oost, Schiphol Oost, Hangar 9", 
       "id": "57340380"
     }, 
     {
       "lat": "4.79809288638105", 
       "lon": "52.3023638565146", 
       "name": "schiphol oost, Schiphol Oost, Hangar 9", 
       "id": "57340390"
     }, 
     {
       "lat": "4.79100336291574", 
       "lon": "52.2953177626629", 
       "name": "schiphol oost, Schiphol Oost, Zuideinde", 
       "id": "57340430"
     }, 
     {
       "lat": "4.79435611164465", 
       "lon": "52.3000263056214", 
       "name": "schiphol oost, Schiphol Oost, ELTA-straat", 
       "id": "57340460"
     }, 
     {
       "lat": "4.78842066241513", 
       "lon": "52.2966079604521", 
       "name": "schiphol oost, Schiphol Oost, Hangar 11", 
       "id": "57340470"
     }, 
     {
       "lat": "4.80160480869607", 
       "lon": "52.3051046287476", 
       "name": "schiphol oost, Schiphol Oost, Hangar 14", 
       "id": "57340500"
     }, 
     {
       "lat": "4.80207278520979", 
       "lon": "52.3051968237911", 
       "name": "schiphol oost, Schiphol Oost, Hangar 14", 
       "id": "57340510"
     }, 
     {
       "lat": "4.80819531097331", 
       "lon": "52.3146821997632", 
       "name": "schiphol oost, Schiphol Oost, Bussluis", 
       "id": "57340530"
     }, 
     {
       "lat": "4.80721842592206", 
       "lon": "52.3153694797835", 
       "name": "schiphol oost, Schiphol Oost, Bussluis", 
       "id": "57340540"
     }, 
     {
       "lat": "4.81019268194878", 
       "lon": "52.3088138925029", 
       "name": "schiphol oost, Schiphol Oost, Stationsplein", 
       "id": "57340580"
     }, 
     {
       "lat": "4.78712742540353", 
       "lon": "52.297931615971", 
       "name": "schiphol oost, Schiphol Oost, Hangar 11 airside", 
       "id": "57340590"
     }, 
     {
       "lat": "4.78727364996893", 
       "lon": "52.2979593216041", 
       "name": "schiphol oost, Schiphol Oost, Hangar 11 airside", 
       "id": "57340600"
     }, 
     {
       "lat": "4.79496774146466", 
       "lon": "52.3003349587848", 
       "name": "schiphol oost, Schiphol Oost, ELTA-straat", 
       "id": "57340610"
     }, 
     {
       "lat": "4.79026561617006", 
       "lon": "52.3000416807224", 
       "name": "schiphol oost, Schiphol Oost, Motorenafdeling", 
       "id": "57340620"
     }, 
     {
       "lat": "4.81289121535447", 
       "lon": "52.3110470304721", 
       "name": "schiphol oost, Schiphol Oost, Gebouw 133", 
       "id": "57342081"
     }, 
     {
       "lat": "4.82188641266706", 
       "lon": "52.2921259370793", 
       "name": "aalsmeer, Aalsmeer, Camping A'damse Bos", 
       "id": "57342230"
     }, 
     {
       "lat": "4.82149492423448", 
       "lon": "52.2929419633273", 
       "name": "aalsmeer, Aalsmeer, Camping A'damse Bos", 
       "id": "57342240"
     }, 
     {
       "lat": "4.81756157797122", 
       "lon": "52.2967609116393", 
       "name": "aalsmeer, Aalsmeer, Rietwijkeroordweg", 
       "id": "57342250"
     }, 
     {
       "lat": "4.81697652255472", 
       "lon": "52.2978006872983", 
       "name": "aalsmeer, Aalsmeer, Rietwijkeroordweg", 
       "id": "57342260"
     }, 
     {
       "lat": "4.79882804451591", 
       "lon": "52.3022057341181", 
       "name": "oude meer, Oude Meer, Hangar 9/10", 
       "id": "57342270"
     }, 
     {
       "lat": "4.79731029394453", 
       "lon": "52.3016768755478", 
       "name": "oude meer, Oude Meer, Hangar 9/10", 
       "id": "57342280"
     }, 
     {
       "lat": "4.79160211684424", 
       "lon": "52.2932984994084", 
       "name": "oude meer, Oude Meer, Fokker", 
       "id": "57342330"
     }, 
     {
       "lat": "4.78993004768912", 
       "lon": "52.2922834188836", 
       "name": "oude meer, Oude Meer, Fokker", 
       "id": "57342340"
     }, 
     {
       "lat": "4.78083703134561", 
       "lon": "52.28620623864", 
       "name": "oude meer, Oude Meer, Breguetlaan", 
       "id": "57342350"
     }, 
     {
       "lat": "4.78071832068304", 
       "lon": "52.2863134849916", 
       "name": "oude meer, Oude Meer, Breguetlaan", 
       "id": "57342360"
     }, 
     {
       "lat": "4.76324950451671", 
       "lon": "52.2924961716097", 
       "name": "ONBEKEND, Schiphol-ZO, Shannonweg", 
       "id": "57342460"
     }, 
     {
       "lat": "4.76487177697427", 
       "lon": "52.2928372744634", 
       "name": "ONBEKEND, Schiphol-ZO, Shannonweg", 
       "id": "57342470"
     }, 
     {
       "lat": "4.77125486644297", 
       "lon": "52.2955221353134", 
       "name": "ONBEKEND, Schiphol-ZO, Anchoragelaan", 
       "id": "57342510"
     }, 
     {
       "lat": "4.77125486644297", 
       "lon": "52.2955221353134", 
       "name": "ONBEKEND, Schiphol-ZO, Anchoragelaan", 
       "id": "57342515"
     }, 
     {
       "lat": "4.76815210922023", 
       "lon": "52.2941128038645", 
       "name": "ONBEKEND, Schiphol-ZO, Ganderweg", 
       "id": "57342540"
     }, 
     {
       "lat": "4.82145064956335", 
       "lon": "52.2883579230537", 
       "name": "aalsmeer, Aalsmeer, Aalsmeerderweg 481", 
       "id": "57342600"
     }, 
     {
       "lat": "4.82143736605385", 
       "lon": "52.2882500046596", 
       "name": "aalsmeer, Aalsmeer, Aalsmeerderweg 481", 
       "id": "57342610"
     }, 
     {
       "lat": "4.81455628556119", 
       "lon": "52.2865271524863", 
       "name": "aalsmeer, Aalsmeer, 417/Kolk", 
       "id": "57342620"
     }, 
     {
       "lat": "4.81562264539658", 
       "lon": "52.2868019495584", 
       "name": "aalsmeer, Aalsmeer, 417/Kolk", 
       "id": "57342630"
     }, 
     {
       "lat": "4.8085163127147", 
       "lon": "52.2844035607941", 
       "name": "aalsmeer, Aalsmeer, 377/Kammeraad", 
       "id": "57342640"
     }, 
     {
       "lat": "4.80815299467009", 
       "lon": "52.2841680960979", 
       "name": "aalsmeer, Aalsmeer, 377/Kammeraad", 
       "id": "57342650"
     }, 
     {
       "lat": "4.80301674413299", 
       "lon": "52.2824620876064", 
       "name": "aalsmeer, Aalsmeer, Kerkweg", 
       "id": "57342660"
     }, 
     {
       "lat": "4.80333900927811", 
       "lon": "52.2824726674517", 
       "name": "aalsmeer, Aalsmeer, Kerkweg", 
       "id": "57342670"
     }, 
     {
       "lat": "4.79725485400056", 
       "lon": "52.2804471439859", 
       "name": "aalsmeer, Aalsmeer, Julianalaan", 
       "id": "57342680"
     }, 
     {
       "lat": "4.79737291316195", 
       "lon": "52.2803848175183", 
       "name": "aalsmeer, Aalsmeer, Julianalaan", 
       "id": "57342690"
     }, 
     {
       "lat": "4.78907230431018", 
       "lon": "52.2775928037069", 
       "name": "aalsmeer, Aalsmeer, Machineweg", 
       "id": "57342700"
     }, 
     {
       "lat": "4.7907074388377", 
       "lon": "52.2780414745557", 
       "name": "aalsmeer, Aalsmeer, Machineweg", 
       "id": "57342710"
     }, 
     {
       "lat": "4.8078539277021", 
       "lon": "52.3149951035894", 
       "name": "schiphol oost, Schiphol Oost, Bussluis", 
       "id": "57342720"
     }, 
     {
       "lat": "4.82627872385652", 
       "lon": "52.2913649072839", 
       "name": "bovenkerk, Bovenkerk, Schinkeldijkje", 
       "id": "57342740"
     }, 
     {
       "lat": "4.77599258654226", 
       "lon": "52.2729240687232", 
       "name": "aalsmeer, Aalsmeer, Middenweg", 
       "id": "57342780"
     }, 
     {
       "lat": "4.78332633042332", 
       "lon": "52.2755772552971", 
       "name": "aalsmeer, Aalsmeer, Aalsmeerderweg 142", 
       "id": "57342790"
     }, 
     {
       "lat": "4.78367772176786", 
       "lon": "52.2755970256911", 
       "name": "aalsmeer, Aalsmeer, Aalsmeerderweg 142", 
       "id": "57342800"
     }, 
     {
       "lat": "4.7607115202884", 
       "lon": "52.2822454794508", 
       "name": "schiphol rijk, Schiphol Rijk, Bellsingel", 
       "id": "57342820"
     }, 
     {
       "lat": "4.76656678222254", 
       "lon": "52.2848199519091", 
       "name": "schiphol rijk, Schiphol Rijk, Koolhovenlaan", 
       "id": "57342880"
     }, 
     {
       "lat": "4.76009784280683", 
       "lon": "52.282116394514", 
       "name": "schiphol rijk, Schiphol Rijk, Bellsingel", 
       "id": "57342900"
     }, 
     {
       "lat": "4.75688246601055", 
       "lon": "52.2815060900394", 
       "name": "schiphol rijk, Schiphol Rijk, Tupolevlaan", 
       "id": "57342910"
     }, 
     {
       "lat": "4.75172147949565", 
       "lon": "52.277586671097", 
       "name": "schiphol rijk, Schiphol Rijk, Boeingavenue", 
       "id": "57342930"
     }, 
     {
       "lat": "4.75196940926885", 
       "lon": "52.2776688953398", 
       "name": "schiphol rijk, Schiphol Rijk, Boeingavenue", 
       "id": "57342940"
     }, 
     {
       "lat": "4.75353057961648", 
       "lon": "52.2791692766776", 
       "name": "schiphol rijk, Schiphol Rijk, Tupolevlaan/Boeingav.", 
       "id": "57342950"
     }, 
     {
       "lat": "4.75592389169343", 
       "lon": "52.280898782", 
       "name": "schiphol rijk, Schiphol Rijk, Tupolevlaan", 
       "id": "57342960"
     }, 
     {
       "lat": "4.75341310280192", 
       "lon": "52.2791866228625", 
       "name": "schiphol rijk, Schiphol Rijk, Tupolevlaan/Boeingav.", 
       "id": "57342970"
     }, 
     {
       "lat": "4.76292701114295", 
       "lon": "52.2831020665003", 
       "name": "schiphol rijk, Schiphol Rijk, Douglassingel", 
       "id": "57342980"
     }, 
     {
       "lat": "4.763102731836", 
       "lon": "52.2831119821796", 
       "name": "schiphol rijk, Schiphol Rijk, Douglassingel", 
       "id": "57342990"
     }, 
     {
       "lat": "4.76713241676197", 
       "lon": "52.2852453532792", 
       "name": "schiphol rijk, Schiphol Rijk, Koolhovenlaan", 
       "id": "57343000"
     }, 
     {
       "lat": "4.788215081365", 
       "lon": "52.2966338830483", 
       "name": "schiphol oost, Schiphol Oost, Hangar 11", 
       "id": "57343090"
     }, 
     {
       "lat": "4.79053358346703", 
       "lon": "52.2953693206881", 
       "name": "schiphol oost, Schiphol Oost, Zuideinde", 
       "id": "57343120"
     }, 
     {
       "lat": "4.97450281276495", 
       "lon": "52.2716805903375", 
       "name": "abcoude, Abcoude, Hoogstraat", 
       "id": "57352020"
     }, 
     {
       "lat": "4.97243824876156", 
       "lon": "52.2731204077255", 
       "name": "abcoude, Abcoude, Dr. van Doornplein", 
       "id": "57352060"
     }, 
     {
       "lat": "4.97078481551456", 
       "lon": "52.2760176674209", 
       "name": "abcoude, Abcoude, Koningsvaren", 
       "id": "57352080"
     }, 
     {
       "lat": "4.97281774659146", 
       "lon": "52.2685559137703", 
       "name": "abcoude, Abcoude, Burg. des Tombeweg", 
       "id": "57352180"
     }, 
     {
       "lat": "4.7117354867272", 
       "lon": "52.2928512646588", 
       "name": "hoofddorp, Hoofddorp, Siriusdreef", 
       "id": "57430010"
     }, 
     {
       "lat": "4.71230118450328", 
       "lon": "52.2922792643753", 
       "name": "hoofddorp, Hoofddorp, Siriusdreef", 
       "id": "57430020"
     }, 
     {
       "lat": "4.70741167602208", 
       "lon": "52.2928264856352", 
       "name": "hoofddorp, Hoofddorp, Wegalaan", 
       "id": "57430030"
     }, 
     {
       "lat": "4.70799263503988", 
       "lon": "52.2922186415617", 
       "name": "hoofddorp, Hoofddorp, Wegalaan", 
       "id": "57430040"
     }, 
     {
       "lat": "4.72023865590953", 
       "lon": "52.2908053361502", 
       "name": "de hoek, De Hoek, Kromhout", 
       "id": "57430070"
     }, 
     {
       "lat": "4.72053528659188", 
       "lon": "52.2905733217063", 
       "name": "de hoek, De Hoek, Kromhout", 
       "id": "57430080"
     }, 
     {
       "lat": "4.72765799936671", 
       "lon": "52.2876652128627", 
       "name": "rozenburg, Rozenburg, Kruisweg", 
       "id": "57430095"
     }, 
     {
       "lat": "4.69874324728767", 
       "lon": "52.2922280646826", 
       "name": "hoofddorp, Hoofddorp, Station", 
       "id": "57430101"
     }, 
     {
       "lat": "4.6985060939352", 
       "lon": "52.2923974553939", 
       "name": "hoofddorp, Hoofddorp, Station", 
       "id": "57430104"
     }, 
     {
       "lat": "4.69816536564609", 
       "lon": "52.2926291580239", 
       "name": "hoofddorp, Hoofddorp, Station", 
       "id": "57430107"
     }, 
     {
       "lat": "4.71678020731944", 
       "lon": "52.2927002157189", 
       "name": "de hoek, De Hoek, Rijnlanderweg", 
       "id": "57430110"
     }, 
     {
       "lat": "4.71607192486016", 
       "lon": "52.2930107767798", 
       "name": "de hoek, De Hoek, Rijnlanderweg", 
       "id": "57430120"
     }, 
     {
       "lat": "4.70885853003084", 
       "lon": "52.2892665660854", 
       "name": "hoofddorp, Hoofddorp, Beukenhorst", 
       "id": "57430730"
     }, 
     {
       "lat": "4.72024728449104", 
       "lon": "52.2902301545051", 
       "name": "ONBEKEND, De Hoek", 
       "id": "57430750"
     }, 
     {
       "lat": "4.69896282039052", 
       "lon": "52.292247318921", 
       "name": "hoofddorp, Hoofddorp, Station", 
       "id": "57430760"
     }, 
     {
       "lat": "4.70982046834469", 
       "lon": "52.2886608980475", 
       "name": "hoofddorp, Hoofddorp, Beukenhorst", 
       "id": "57430780"
     }, 
     {
       "lat": "4.72090128917363", 
       "lon": "52.290602348691", 
       "name": "ONBEKEND, De Hoek", 
       "id": "57430800"
     }, 
     {
       "lat": "4.70476307115825", 
       "lon": "52.2629261035568", 
       "name": "rijsenhout, Rijsenhout, Konnetlaantje", 
       "id": "57432170"
     }, 
     {
       "lat": "4.72741779396551", 
       "lon": "52.2870616784639", 
       "name": "rozenburg, Rozenburg, Kruisweg", 
       "id": "57432325"
     }, 
     {
       "lat": "4.73978294543195", 
       "lon": "52.2682642637147", 
       "name": "aalsmeerderbrug, Aalsmeerderbrug, Aalsmeerderdijk 446", 
       "id": "57442010"
     }, 
     {
       "lat": "4.74254671464525", 
       "lon": "52.269627568583", 
       "name": "aalsmeerderbrug, Aalsmeerderbrug, Aalsmeerderdijk 426", 
       "id": "57442090"
     }, 
     {
       "lat": "4.74191900596359", 
       "lon": "52.2694713475891", 
       "name": "aalsmeerderbrug, Aalsmeerderbrug, Aalsmeerderdijk 426", 
       "id": "57442100"
     }, 
     {
       "lat": "4.75111406197551", 
       "lon": "52.2678044822321", 
       "name": "aalsmeer, Aalsmeer, TV-Studio", 
       "id": "57442140"
     }, 
     {
       "lat": "4.75149043704111", 
       "lon": "52.2681210866772", 
       "name": "aalsmeer, Aalsmeer, TV-Studio", 
       "id": "57442150"
     }, 
     {
       "lat": "4.74976256761772", 
       "lon": "52.2660175792281", 
       "name": "aalsmeer, Aalsmeer, Drie Kolommenplein", 
       "id": "57442180"
     }, 
     {
       "lat": "4.75004886381318", 
       "lon": "52.2654618673922", 
       "name": "aalsmeer, Aalsmeer, Drie Kolommenplein", 
       "id": "57442190"
     }, 
     {
       "lat": "4.74678087528187", 
       "lon": "52.2726705486099", 
       "name": "aalsmeerderbrug, Aalsmeerderbrug, Aalsmeerderdijk 380", 
       "id": "57442210"
     }, 
     {
       "lat": "4.74600725270843", 
       "lon": "52.272468619095", 
       "name": "aalsmeerderbrug, Aalsmeerderbrug, Aalsmeerderdijk 380", 
       "id": "57442220"
     }, 
     {
       "lat": "4.75974610793903", 
       "lon": "52.2613433181722", 
       "name": "aalsmeer, Aalsmeer, Gloxiniastraat", 
       "id": "57442230"
     }, 
     {
       "lat": "4.75995698956615", 
       "lon": "52.2609309899064", 
       "name": "aalsmeer, Aalsmeer, Gloxiniastraat", 
       "id": "57442240"
     }, 
     {
       "lat": "4.75995698956615", 
       "lon": "52.2609309899064", 
       "name": "aalsmeer, Aalsmeer, Gloxiniastraat", 
       "id": "57442241"
     }, 
     {
       "lat": "4.7605202682036", 
       "lon": "52.2604576144263", 
       "name": "aalsmeer, Aalsmeer, Gloxiniastraat", 
       "id": "57442250"
     }, 
     {
       "lat": "4.7605202682036", 
       "lon": "52.2604576144263", 
       "name": "aalsmeer, Aalsmeer, Gloxiniastraat", 
       "id": "57442251"
     }, 
     {
       "lat": "4.76252352694981", 
       "lon": "52.2586166932344", 
       "name": "aalsmeer, Aalsmeer, Zwarteweg", 
       "id": "57442260"
     }, 
     {
       "lat": "4.76252352694981", 
       "lon": "52.2586166932344", 
       "name": "aalsmeer, Aalsmeer, Zwarteweg", 
       "id": "57442261"
     }, 
     {
       "lat": "4.76262945341109", 
       "lon": "52.2583745772256", 
       "name": "aalsmeer, Aalsmeer, Zwarteweg", 
       "id": "57442270"
     }, 
     {
       "lat": "4.76246683610864", 
       "lon": "52.2584815736417", 
       "name": "aalsmeer, Aalsmeer, Zwarteweg", 
       "id": "57442271"
     }, 
     {
       "lat": "4.76838628810464", 
       "lon": "52.2604361467251", 
       "name": "aalsmeer, Aalsmeer, Mendelstraat", 
       "id": "57442280"
     }, 
     {
       "lat": "4.76926257904897", 
       "lon": "52.2606204914569", 
       "name": "aalsmeer, Aalsmeer, Mendelstraat", 
       "id": "57442290"
     }, 
     {
       "lat": "4.76924008860737", 
       "lon": "52.2706779213593", 
       "name": "aalsmeer, Aalsmeer, Stommeerkade", 
       "id": "57442390"
     }, 
     {
       "lat": "4.76878906749219", 
       "lon": "52.2704508633454", 
       "name": "aalsmeer, Aalsmeer, Stommeerkade", 
       "id": "57442420"
     }, 
     {
       "lat": "4.7690047037618", 
       "lon": "52.2675848280315", 
       "name": "aalsmeer, Aalsmeer, Seringenpark", 
       "id": "57442430"
     }, 
     {
       "lat": "4.76916484182384", 
       "lon": "52.2676575692696", 
       "name": "aalsmeer, Aalsmeer, Seringenpark", 
       "id": "57442440"
     }, 
     {
       "lat": "4.77543754797584", 
       "lon": "52.2621446210408", 
       "name": "aalsmeer, Aalsmeer, BVFH Ingang C1-D3", 
       "id": "57442450"
     }, 
     {
       "lat": "4.77553847114946", 
       "lon": "52.2622619871229", 
       "name": "aalsmeer, Aalsmeer, BVFH Ingang C1-D3", 
       "id": "57442460"
     }, 
     {
       "lat": "4.77016582686209", 
       "lon": "52.2514664453847", 
       "name": "aalsmeer, Aalsmeer, Mozartlaan", 
       "id": "57442610"
     }, 
     {
       "lat": "4.77027306477931", 
       "lon": "52.2511254612506", 
       "name": "aalsmeer, Aalsmeer, Mozartlaan", 
       "id": "57442620"
     }, 
     {
       "lat": "4.76638460462791", 
       "lon": "52.2548261289653", 
       "name": "aalsmeer, Aalsmeer, Beethovenlaan", 
       "id": "57442630"
     }, 
     {
       "lat": "4.76644556464653", 
       "lon": "52.2546556772283", 
       "name": "aalsmeer, Aalsmeer, Beethovenlaan", 
       "id": "57442640"
     }, 
     {
       "lat": "4.7580561776042", 
       "lon": "52.2627634249739", 
       "name": "aalsmeer, Aalsmeer, Hortensiaplein", 
       "id": "57442660"
     }, 
     {
       "lat": "4.75760542099474", 
       "lon": "52.2625273368483", 
       "name": "aalsmeer, Aalsmeer, Hortensiaplein", 
       "id": "57442661"
     }, 
     {
       "lat": "4.7577192922404", 
       "lon": "52.2627616311768", 
       "name": "aalsmeer, Aalsmeer, Hortensiaplein", 
       "id": "57442662"
     }, 
     {
       "lat": "4.75827931522034", 
       "lon": "52.2625219368102", 
       "name": "aalsmeer, Aalsmeer, Hortensiaplein", 
       "id": "57442663"
     }, 
     {
       "lat": "4.75776895469946", 
       "lon": "52.2623574360409", 
       "name": "aalsmeer, Aalsmeer, Hortensiaplein", 
       "id": "57442664"
     }, 
     {
       "lat": "4.74957971666525", 
       "lon": "52.2736653688795", 
       "name": "aalsmeer, Aalsmeer, Aalsmeerderbrug", 
       "id": "57442670"
     }, 
     {
       "lat": "4.78585902998111", 
       "lon": "52.2638159394002", 
       "name": "aalsmeer, Aalsmeer, BVFH Ingang B4-B5", 
       "id": "57442720"
     }, 
     {
       "lat": "4.76298158946795", 
       "lon": "52.2645961265728", 
       "name": "aalsmeer, Aalsmeer, Spoorlaan", 
       "id": "57442760"
     }, 
     {
       "lat": "4.76141743468147", 
       "lon": "52.2643631556693", 
       "name": "aalsmeer, Aalsmeer, Spoorlaan", 
       "id": "57442770"
     }, 
     {
       "lat": "4.76407517097896", 
       "lon": "52.2628672160048", 
       "name": "aalsmeer, Aalsmeer, J.C. Mensinglaan", 
       "id": "57442780"
     }, 
     {
       "lat": "4.77629740990287", 
       "lon": "52.2731323675369", 
       "name": "aalsmeer, Aalsmeer, Middenweg", 
       "id": "57442790"
     }, 
     {
       "lat": "4.77862152501656", 
       "lon": "52.2638957382242", 
       "name": "aalsmeer, Aalsmeer, BVFH Ingang C3-C4", 
       "id": "57442800"
     }, 
     {
       "lat": "4.77227764187693", 
       "lon": "52.261849595144", 
       "name": "aalsmeer, Aalsmeer, P.F.von Sieboldlaan", 
       "id": "57442880"
     }, 
     {
       "lat": "4.77268713513469", 
       "lon": "52.2618966649105", 
       "name": "aalsmeer, Aalsmeer, P.F.von Sieboldlaan", 
       "id": "57442890"
     }, 
     {
       "lat": "4.78501244031545", 
       "lon": "52.2646744740873", 
       "name": "aalsmeer, Aalsmeer, BVFH Ingang B4-B5", 
       "id": "57442910"
     }, 
     {
       "lat": "4.77855000808699", 
       "lon": "52.263769538316", 
       "name": "aalsmeer, Aalsmeer, BVFH Ingang C3-C4", 
       "id": "57442930"
     }, 
     {
       "lat": "4.78674903053292", 
       "lon": "52.2586523798899", 
       "name": "aalsmeer, Aalsmeer, BVFH Hoofdingang", 
       "id": "57442960"
     }, 
     {
       "lat": "4.78593949902258", 
       "lon": "52.2589448673752", 
       "name": "aalsmeer, Aalsmeer, BVFH Hoofdingang", 
       "id": "57442970"
     }, 
     {
       "lat": "4.75256951200098", 
       "lon": "52.2366328892402", 
       "name": "kudelstaart, Kudelstaart, Einsteinstraat", 
       "id": "57522060"
     }, 
     {
       "lat": "4.75253033563988", 
       "lon": "52.2363001213453", 
       "name": "kudelstaart, Kudelstaart, Einsteinstraat", 
       "id": "57522070"
     }, 
     {
       "lat": "4.7514975350772", 
       "lon": "52.2348115415806", 
       "name": "kudelstaart, Kudelstaart, Schweitzerstraat", 
       "id": "57522080"
     }, 
     {
       "lat": "4.75047377619234", 
       "lon": "52.2347431118682", 
       "name": "kudelstaart, Kudelstaart, Schweitzerstraat", 
       "id": "57522090"
     }, 
     {
       "lat": "4.74601061061362", 
       "lon": "52.2336044540695", 
       "name": "kudelstaart, Kudelstaart, Gravin Aleidstraat", 
       "id": "57522100"
     }, 
     {
       "lat": "4.745369407176", 
       "lon": "52.2334032349958", 
       "name": "kudelstaart, Kudelstaart, Gravin Aleidstraat", 
       "id": "57522110"
     }, 
     {
       "lat": "4.73477478434812", 
       "lon": "52.2281500980091", 
       "name": "kudelstaart, Kudelstaart, Bilderdammerweg", 
       "id": "57522400"
     }, 
     {
       "lat": "4.73457133237524", 
       "lon": "52.2280501053775", 
       "name": "kudelstaart, Kudelstaart, Bilderdammerweg", 
       "id": "57522410"
     }, 
     {
       "lat": "4.73987523365084", 
       "lon": "52.2307038040473", 
       "name": "kudelstaart, Kudelstaart, Calslager Bancken", 
       "id": "57522420"
     }, 
     {
       "lat": "4.74031289583975", 
       "lon": "52.2308050702102", 
       "name": "kudelstaart, Kudelstaart, Calslager Bancken", 
       "id": "57522430"
     }, 
     {
       "lat": "4.76599954763858", 
       "lon": "52.2435890956997", 
       "name": "kudelstaart, Kudelstaart, Legmeerdijk", 
       "id": "57522460"
     }, 
     {
       "lat": "4.76623417807327", 
       "lon": "52.2435633650078", 
       "name": "kudelstaart, Kudelstaart, Legmeerdijk", 
       "id": "57522470"
     }, 
     {
       "lat": "4.75633034819299", 
       "lon": "52.2388101602974", 
       "name": "kudelstaart, Kudelstaart, De Rietlanden", 
       "id": "57522480"
     }, 
     {
       "lat": "4.75716097371656", 
       "lon": "52.2390842337414", 
       "name": "kudelstaart, Kudelstaart, De Rietlanden", 
       "id": "57522490"
     }, 
     {
       "lat": "4.73959159319277", 
       "lon": "52.2683261314184", 
       "name": "aalsmeerderbrug, Aalsmeerderbrug, Aalsmeerderdijk 446", 
       "id": "57542070"
     }, 
     {
       "lat": "4.73248466066858", 
       "lon": "52.2664444380011", 
       "name": "rijsenhout, Rijsenhout, Aarbergerweg", 
       "id": "57542090"
     }, 
     {
       "lat": "4.73260264079092", 
       "lon": "52.2663911634453", 
       "name": "rijsenhout, Rijsenhout, Aarbergerweg", 
       "id": "57542099"
     }, 
     {
       "lat": "4.72898541417726", 
       "lon": "52.2653194776596", 
       "name": "rijsenhout, Rijsenhout, Aalsmeerderdijk 519", 
       "id": "57542110"
     }, 
     {
       "lat": "4.7290887475382", 
       "lon": "52.2652661250269", 
       "name": "rijsenhout, Rijsenhout, Aalsmeerderdijk 519", 
       "id": "57542119"
     }, 
     {
       "lat": "4.72401720716512", 
       "lon": "52.2625144081973", 
       "name": "rijsenhout, Rijsenhout, Aalsmeerderdijk 583", 
       "id": "57542130"
     }, 
     {
       "lat": "4.72420708290179", 
       "lon": "52.262551425574", 
       "name": "rijsenhout, Rijsenhout, Aalsmeerderdijk 583", 
       "id": "57542139"
     }, 
     {
       "lat": "4.72111445752694", 
       "lon": "52.259738761279", 
       "name": "rijsenhout, Rijsenhout, Verremeer", 
       "id": "57542150"
     }, 
     {
       "lat": "4.72130526039165", 
       "lon": "52.2597128724466", 
       "name": "rijsenhout, Rijsenhout, Verremeer", 
       "id": "57542159"
     }, 
     {
       "lat": "4.70546002307665", 
       "lon": "52.2623728678689", 
       "name": "rijsenhout, Rijsenhout, Konnetlaantje", 
       "id": "57542160"
     }, 
     {
       "lat": "4.71803053226532", 
       "lon": "52.260269609165", 
       "name": "rijsenhout, Rijsenhout, Jolweg", 
       "id": "57542250"
     }, 
     {
       "lat": "4.7184414383922", 
       "lon": "52.2602180069332", 
       "name": "rijsenhout, Rijsenhout, Jolweg", 
       "id": "57542270"
     }, 
     {
       "lat": "4.71102019691488", 
       "lon": "52.2608498813076", 
       "name": "rijsenhout, Rijsenhout, Drakenstraat", 
       "id": "57542290"
     }, 
     {
       "lat": "4.71165959250665", 
       "lon": "52.2611860950013", 
       "name": "rijsenhout, Rijsenhout, Drakenstraat", 
       "id": "57542300"
     }, 
     {
       "lat": "5.0608070517798", 
       "lon": "52.3282316708905", 
       "name": "muiden, Muiden, P&R terrein", 
       "id": "58200120"
     }, 
     {
       "lat": "5.0605348779302", 
       "lon": "52.3273411369192", 
       "name": "muiden, Muiden, Vechtbrug / A 1", 
       "id": "58200130"
     }, 
     {
       "lat": "4.9113514786664", 
       "lon": "52.2995752408853", 
       "name": "ONBEKEND, Ouderkerk a/d Amstel", 
       "id": "58252000"
     }, 
     {
       "lat": "4.91098421768806", 
       "lon": "52.2996456652824", 
       "name": "ONBEKEND, Ouderkerk a/d Amstel", 
       "id": "58252010"
     }, 
     {
       "lat": "4.910823732031", 
       "lon": "52.2995731163467", 
       "name": "ouderkerk a/d amstel, Ouderkerk a/d Amstel, J. van Ruisdaelweg", 
       "id": "58252050"
     }, 
     {
       "lat": "4.9110596338126", 
       "lon": "52.2994482367114", 
       "name": "ouderkerk a/d amstel, Ouderkerk a/d Amstel, J. van Ruisdaelweg", 
       "id": "58252060"
     }, 
     {
       "lat": "4.90047817900551", 
       "lon": "52.2991535036673", 
       "name": "ouderkerk a/d amstel, Ouderkerk a/d Amstel, Brug/Hoger Einde", 
       "id": "58252070"
     }, 
     {
       "lat": "4.90094777366646", 
       "lon": "52.299110496154", 
       "name": "ouderkerk a/d amstel, Ouderkerk a/d Amstel, Brug/Hoger Einde", 
       "id": "58252080"
     }, 
     {
       "lat": "4.8977181287654", 
       "lon": "52.2981804140397", 
       "name": "ouderkerk a/d amstel, Ouderkerk a/d Amstel, Brug/Amsteldijk", 
       "id": "58252090"
     }, 
     {
       "lat": "4.89780855719486", 
       "lon": "52.2979560923234", 
       "name": "ouderkerk a/d amstel, Ouderkerk a/d Amstel, Brug/Amsteldijk", 
       "id": "58252100"
     }, 
     {
       "lat": "4.82552015821428", 
       "lon": "52.2539445679071", 
       "name": "amstelveen, Amstelveen, Hoeve Brasil", 
       "id": "58342030"
     }, 
     {
       "lat": "4.83895627308019", 
       "lon": "52.2772055106392", 
       "name": "amstelveen, Amstelveen, Nesserlaan", 
       "id": "58342050"
     }, 
     {
       "lat": "4.83672932785493", 
       "lon": "52.270076731558", 
       "name": "amstelveen, Amstelveen, J.C. van Hattumweg", 
       "id": "58342060"
     }, 
     {
       "lat": "4.83648183936587", 
       "lon": "52.2699497478543", 
       "name": "amstelveen, Amstelveen, J.C. van Hattumweg", 
       "id": "58342070"
     }, 
     {
       "lat": "4.83372409971267", 
       "lon": "52.2643373868541", 
       "name": "amstelveen, Amstelveen, Zijdelweg", 
       "id": "58342080"
     }, 
     {
       "lat": "4.83338775799362", 
       "lon": "52.2642908717163", 
       "name": "amstelveen, Amstelveen, Zijdelweg", 
       "id": "58342090"
     }, 
     {
       "lat": "4.830983021861", 
       "lon": "52.2609630299559", 
       "name": "amstelveen, Amstelveen, Christinahoeve", 
       "id": "58342100"
     }, 
     {
       "lat": "4.83038880240696", 
       "lon": "52.2604569071507", 
       "name": "amstelveen, Amstelveen, Christinahoeve", 
       "id": "58342110"
     }, 
     {
       "lat": "4.82588400223508", 
       "lon": "52.2541260558127", 
       "name": "amstelveen, Amstelveen, Hoeve Brasil", 
       "id": "58342120"
     }, 
     {
       "lat": "4.85184446918408", 
       "lon": "52.2424273562612", 
       "name": "uithoorn, Uithoorn, Rode Paal", 
       "id": "58352000"
     }, 
     {
       "lat": "4.85468943191155", 
       "lon": "52.2444984542172", 
       "name": "nes a/d amstel, Nes a/d Amstel, Amsteldijk 204", 
       "id": "58352030"
     }, 
     {
       "lat": "4.85489516344161", 
       "lon": "52.2444364655202", 
       "name": "nes a/d amstel, Nes a/d Amstel, Amsteldijk 204", 
       "id": "58352031"
     }, 
     {
       "lat": "4.85649675115821", 
       "lon": "52.2476523681486", 
       "name": "nes a/d amstel, Nes a/d Amstel, Amsteldijk 202", 
       "id": "58352050"
     }, 
     {
       "lat": "4.85668785237315", 
       "lon": "52.2475903106197", 
       "name": "nes a/d amstel, Nes a/d Amstel, Amsteldijk 202", 
       "id": "58352051"
     }, 
     {
       "lat": "4.86128428627459", 
       "lon": "52.248959048625", 
       "name": "nes a/d amstel, Nes a/d Amstel, Amsteldijk 199", 
       "id": "58352070"
     }, 
     {
       "lat": "4.8614606374755", 
       "lon": "52.2489059056901", 
       "name": "nes a/d amstel, Nes a/d Amstel, Amsteldijk 199", 
       "id": "58352071"
     }, 
     {
       "lat": "4.86763805519394", 
       "lon": "52.2516026449369", 
       "name": "nes a/d amstel, Nes a/d Amstel, Nessersluis", 
       "id": "58352080"
     }, 
     {
       "lat": "4.86759317977088", 
       "lon": "52.2516833390431", 
       "name": "nes a/d amstel, Nes a/d Amstel, Nessersluis", 
       "id": "58352090"
     }, 
     {
       "lat": "4.87223186370228", 
       "lon": "52.2570604485296", 
       "name": "nes a/d amstel, Nes a/d Amstel, Porceleinhuisje", 
       "id": "58352110"
     }, 
     {
       "lat": "4.87232025686033", 
       "lon": "52.2570158940369", 
       "name": "nes a/d amstel, Nes a/d Amstel, Porceleinhuisje", 
       "id": "58352111"
     }, 
     {
       "lat": "4.8726592763307", 
       "lon": "52.2593632177881", 
       "name": "nes a/d amstel, Nes a/d Amstel, Kerklaan", 
       "id": "58352130"
     }, 
     {
       "lat": "4.87287897096499", 
       "lon": "52.259364174026", 
       "name": "nes a/d amstel, Nes a/d Amstel, Kerklaan", 
       "id": "58352131"
     }, 
     {
       "lat": "4.87434897017415", 
       "lon": "52.2614467703731", 
       "name": "nes a/d amstel, Nes a/d Amstel, R.K. Kerk", 
       "id": "58352150"
     }, 
     {
       "lat": "4.87445243114769", 
       "lon": "52.2613663280238", 
       "name": "nes a/d amstel, Nes a/d Amstel, R.K. Kerk", 
       "id": "58352151"
     }, 
     {
       "lat": "4.87832781673553", 
       "lon": "52.2619133634049", 
       "name": "nes a/d amstel, Nes a/d Amstel, Amsteldijk 128", 
       "id": "58352170"
     }, 
     {
       "lat": "4.87840238837984", 
       "lon": "52.2617968415955", 
       "name": "nes a/d amstel, Nes a/d Amstel, Amsteldijk 128", 
       "id": "58352171"
     }, 
     {
       "lat": "4.88136853993631", 
       "lon": "52.2637329850941", 
       "name": "nes a/d amstel, Nes a/d Amstel, Parelmolen", 
       "id": "58352190"
     }, 
     {
       "lat": "4.88147148285375", 
       "lon": "52.2636974739688", 
       "name": "nes a/d amstel, Nes a/d Amstel, Parelmolen", 
       "id": "58352191"
     }, 
     {
       "lat": "4.88022265978035", 
       "lon": "52.2704510258098", 
       "name": "nes a/d amstel, Nes a/d Amstel, Nesserlaan", 
       "id": "58352210"
     }, 
     {
       "lat": "4.88036895474765", 
       "lon": "52.2704696289304", 
       "name": "nes a/d amstel, Nes a/d Amstel, Nesserlaan", 
       "id": "58352211"
     }, 
     {
       "lat": "4.81465248603691", 
       "lon": "52.2403475343096", 
       "name": "uithoorn, Uithoorn, Watsonweg", 
       "id": "58442000"
     }, 
     {
       "lat": "4.82322330586285", 
       "lon": "52.2468151602515", 
       "name": "uithoorn, Uithoorn, Joost v/d Vondellaan", 
       "id": "58442080"
     }, 
     {
       "lat": "4.83425266282777", 
       "lon": "52.2300507809289", 
       "name": "amstelhoek, Amstelhoek, Piet Heinlaan", 
       "id": "58442130"
     }, 
     {
       "lat": "4.8420144583054", 
       "lon": "52.2285319350733", 
       "name": "amstelhoek, Amstelhoek, Tienboerenweg", 
       "id": "58442150"
     }, 
     {
       "lat": "4.82978788850137", 
       "lon": "52.2441139672087", 
       "name": "uithoorn, Uithoorn, Achterberglaan", 
       "id": "58442200"
     }, 
     {
       "lat": "4.82977549774779", 
       "lon": "52.2439341493242", 
       "name": "uithoorn, Uithoorn, Achterberglaan", 
       "id": "58442210"
     }, 
     {
       "lat": "4.83376193194863", 
       "lon": "52.2471615925584", 
       "name": "uithoorn, Uithoorn, Romeflat", 
       "id": "58442220"
     }, 
     {
       "lat": "4.83340559953929", 
       "lon": "52.2475553934873", 
       "name": "uithoorn, Uithoorn, Romeflat", 
       "id": "58442230"
     }, 
     {
       "lat": "4.82739202056562", 
       "lon": "52.2495044094594", 
       "name": "uithoorn, Uithoorn, Heijermanslaan", 
       "id": "58442240"
     }, 
     {
       "lat": "4.82978602876464", 
       "lon": "52.2489404969215", 
       "name": "uithoorn, Uithoorn, Heijermanslaan", 
       "id": "58442250"
     }, 
     {
       "lat": "4.82483460633285", 
       "lon": "52.2502472553826", 
       "name": "uithoorn, Uithoorn, Willem Klooslaan", 
       "id": "58442260"
     }, 
     {
       "lat": "4.82189455090337", 
       "lon": "52.2511320237026", 
       "name": "uithoorn, Uithoorn, Op de Klucht", 
       "id": "58442270"
     }, 
     {
       "lat": "4.82130869668387", 
       "lon": "52.2511382076036", 
       "name": "uithoorn, Uithoorn, Op de Klucht", 
       "id": "58442280"
     }, 
     {
       "lat": "4.81880447519243", 
       "lon": "52.2499937049554", 
       "name": "uithoorn, Uithoorn, In het Midden", 
       "id": "58442290"
     }, 
     {
       "lat": "4.81897950429311", 
       "lon": "52.2500484745375", 
       "name": "uithoorn, Uithoorn, In het Midden", 
       "id": "58442300"
     }, 
     {
       "lat": "4.82748572819162", 
       "lon": "52.2327332867775", 
       "name": "uithoorn, Uithoorn, Amstelplein", 
       "id": "58442310"
     }, 
     {
       "lat": "4.81943120810124", 
       "lon": "52.2479294847349", 
       "name": "uithoorn, Uithoorn, Aan de Zoom", 
       "id": "58442320"
     }, 
     {
       "lat": "4.8516974136776", 
       "lon": "52.2424806176346", 
       "name": "uithoorn, Uithoorn, Rode Paal", 
       "id": "58442330"
     }, 
     {
       "lat": "4.82381068861747", 
       "lon": "52.2513119458976", 
       "name": "uithoorn, Uithoorn, Arth.v.Schendellaan", 
       "id": "58442340"
     }, 
     {
       "lat": "4.80953321177097", 
       "lon": "52.2365746220206", 
       "name": "uithoorn, Uithoorn, Korte Polder", 
       "id": "58442380"
     }, 
     {
       "lat": "4.80954765189486", 
       "lon": "52.2332041925574", 
       "name": "uithoorn, Uithoorn, Rietgans", 
       "id": "58442410"
     }, 
     {
       "lat": "4.83543196616071", 
       "lon": "52.2376511419164", 
       "name": "uithoorn, Uithoorn, Industrieweg", 
       "id": "58442430"
     }, 
     {
       "lat": "4.83521237976864", 
       "lon": "52.2376501161983", 
       "name": "uithoorn, Uithoorn, Industrieweg", 
       "id": "58442440"
     }, 
     {
       "lat": "4.83705342060625", 
       "lon": "52.2332006648395", 
       "name": "amstelhoek, Amstelhoek, Amstelkade", 
       "id": "58442470"
     }, 
     {
       "lat": "4.83688940826734", 
       "lon": "52.2334425765291", 
       "name": "amstelhoek, Amstelhoek, Amstelkade", 
       "id": "58442480"
     }, 
     {
       "lat": "4.80913575063641", 
       "lon": "52.2367434498901", 
       "name": "uithoorn, Uithoorn, Korte Polder", 
       "id": "58442490"
     }, 
     {
       "lat": "4.84199883215573", 
       "lon": "52.228612754854", 
       "name": "amstelhoek, Amstelhoek, Tienboerenweg", 
       "id": "58442500"
     }, 
     {
       "lat": "4.83643116001834", 
       "lon": "52.2349863741468", 
       "name": "uithoorn, Uithoorn, Wilhelminakade", 
       "id": "58442510"
     }, 
     {
       "lat": "4.83656368184863", 
       "lon": "52.2349240760086", 
       "name": "uithoorn, Uithoorn, Wilhelminakade", 
       "id": "58442511"
     }, 
     {
       "lat": "4.83944557560145", 
       "lon": "52.2362766817146", 
       "name": "uithoorn, Uithoorn, Ned.Herv. Kerk", 
       "id": "58442540"
     }, 
     {
       "lat": "4.83975298724701", 
       "lon": "52.2362781065749", 
       "name": "uithoorn, Uithoorn, Ned.Herv. Kerk", 
       "id": "58442541"
     }, 
     {
       "lat": "4.84344076501279", 
       "lon": "52.2375894054143", 
       "name": "uithoorn, Uithoorn, Molenlaan", 
       "id": "58442550"
     }, 
     {
       "lat": "4.84325309159269", 
       "lon": "52.2373728301552", 
       "name": "uithoorn, Uithoorn, Molenlaan", 
       "id": "58442551"
     }, 
     {
       "lat": "4.84746311506466", 
       "lon": "52.2403042398661", 
       "name": "uithoorn, Uithoorn, Cindu", 
       "id": "58442570"
     }, 
     {
       "lat": "4.84791510434487", 
       "lon": "52.240459099171", 
       "name": "uithoorn, Uithoorn, Cindu", 
       "id": "58442571"
     }, 
     {
       "lat": "4.8357852054785", 
       "lon": "52.2398638332302", 
       "name": "uithoorn, Uithoorn, Anthony Fokkerweg", 
       "id": "58442610"
     }, 
     {
       "lat": "4.81492567799193", 
       "lon": "52.2407353413165", 
       "name": "uithoorn, Uithoorn, Watsonweg", 
       "id": "58442630"
     }, 
     {
       "lat": "4.83609720226843", 
       "lon": "52.2394967819704", 
       "name": "uithoorn, Uithoorn, Anthony Fokkerweg", 
       "id": "58442640"
     }, 
     {
       "lat": "4.81585933548577", 
       "lon": "52.2330101862414", 
       "name": "uithoorn, Uithoorn, Fort aan de Drecht", 
       "id": "58442650"
     }, 
     {
       "lat": "4.81556508533641", 
       "lon": "52.233125606785", 
       "name": "uithoorn, Uithoorn, Fort aan de Drecht", 
       "id": "58442660"
     }, 
     {
       "lat": "4.82137389687706", 
       "lon": "52.2321828678625", 
       "name": "uithoorn, Uithoorn, Fermoor", 
       "id": "58442670"
     }, 
     {
       "lat": "4.82127017980698", 
       "lon": "52.2322812390101", 
       "name": "uithoorn, Uithoorn, Fermoor", 
       "id": "58442680"
     }, 
     {
       "lat": "4.80812383392023", 
       "lon": "52.2335028140375", 
       "name": "uithoorn, Uithoorn, Rietgans", 
       "id": "58442700"
     }, 
     {
       "lat": "4.82563830758232", 
       "lon": "52.2445796692052", 
       "name": "uithoorn, Uithoorn, Alfons Arienslaan", 
       "id": "58442730"
     }, 
     {
       "lat": "4.82517148614987", 
       "lon": "52.2444426300571", 
       "name": "uithoorn, Uithoorn, Alfons Arienslaan", 
       "id": "58442740"
     }, 
     {
       "lat": "4.8344830503798", 
       "lon": "52.2350761439153", 
       "name": "uithoorn, Uithoorn, Stationsstraat", 
       "id": "58442750"
     }, 
     {
       "lat": "4.83448104260187", 
       "lon": "52.2352379182148", 
       "name": "uithoorn, Uithoorn, Stationsstraat", 
       "id": "58442760"
     }, 
     {
       "lat": "4.82558672058352", 
       "lon": "52.2405438224756", 
       "name": "uithoorn, Uithoorn, Couperuslaan", 
       "id": "58442770"
     }, 
     {
       "lat": "4.82524625698935", 
       "lon": "52.2408388069835", 
       "name": "uithoorn, Uithoorn, Couperuslaan", 
       "id": "58442780"
     }, 
     {
       "lat": "4.82842309816105", 
       "lon": "52.2443591841278", 
       "name": "uithoorn, Uithoorn, Guido Gezellelaan", 
       "id": "58442800"
     }, 
     {
       "lat": "4.82988642324945", 
       "lon": "52.2432605746667", 
       "name": "uithoorn, Uithoorn, Guido Gezellelaan", 
       "id": "58442810"
     }, 
     {
       "lat": "4.86200196064245", 
       "lon": "52.2228791690802", 
       "name": "mijdrecht, Mijdrecht, Eerste/Tweede Zijweg", 
       "id": "58542020"
     }, 
     {
       "lat": "4.86257851881094", 
       "lon": "52.2223873920259", 
       "name": "mijdrecht, Mijdrecht, Eerste/Tweede Zijweg", 
       "id": "58542030"
     }, 
     {
       "lat": "4.87050580303406", 
       "lon": "52.2152319452741", 
       "name": "mijdrecht, Mijdrecht, Hofland", 
       "id": "58542050"
     }, 
     {
       "lat": "4.86940119041765", 
       "lon": "52.2133306408228", 
       "name": "mijdrecht, Mijdrecht, Dukaton", 
       "id": "58542060"
     }, 
     {
       "lat": "4.86922572088169", 
       "lon": "52.2133208833881", 
       "name": "mijdrecht, Mijdrecht, Dukaton", 
       "id": "58542070"
     }, 
     {
       "lat": "4.87173079210223", 
       "lon": "52.2168551362277", 
       "name": "mijdrecht, Mijdrecht, Provincialeweg", 
       "id": "58542200"
     }, 
     {
       "lat": "4.86332260414581", 
       "lon": "52.2138700780456", 
       "name": "mijdrecht, Mijdrecht, Kogger", 
       "id": "58542250"
     }, 
     {
       "lat": "4.86522857282396", 
       "lon": "52.2135459611032", 
       "name": "mijdrecht, Mijdrecht, Kogger", 
       "id": "58542260"
     }, 
     {
       "lat": "4.8614767245099", 
       "lon": "52.2128192676844", 
       "name": "mijdrecht, Mijdrecht, Dokter v.d. Berglaan", 
       "id": "58542270"
     }, 
     {
       "lat": "4.86162409430226", 
       "lon": "52.2127300435834", 
       "name": "mijdrecht, Mijdrecht, Dokter v.d. Berglaan", 
       "id": "58542280"
     }, 
     {
       "lat": "4.86080782693987", 
       "lon": "52.2062730188566", 
       "name": "mijdrecht, Mijdrecht, Prinses Margrietlaan", 
       "id": "58542290"
     }, 
     {
       "lat": "4.86024640616558", 
       "lon": "52.2067378916045", 
       "name": "mijdrecht, Mijdrecht, Prinses Margrietlaan", 
       "id": "58542300"
     }, 
     {
       "lat": "4.86406379538018", 
       "lon": "52.2043281010165", 
       "name": "mijdrecht, Mijdrecht, Proostdijland", 
       "id": "58542310"
     }, 
     {
       "lat": "4.8641655600511", 
       "lon": "52.2043824798841", 
       "name": "mijdrecht, Mijdrecht, Proostdijland", 
       "id": "58542320"
     }, 
     {
       "lat": "4.86843774922366", 
       "lon": "52.203080087454", 
       "name": "mijdrecht, Mijdrecht, Bozenhoven", 
       "id": "58542330"
     }, 
     {
       "lat": "4.86840556489925", 
       "lon": "52.2033316104161", 
       "name": "mijdrecht, Mijdrecht, Bozenhoven", 
       "id": "58542340"
     }, 
     {
       "lat": "4.87057971646504", 
       "lon": "52.2012828873979", 
       "name": "mijdrecht, Mijdrecht, Dr.Schaepmanplantsoen", 
       "id": "58542350"
     }, 
     {
       "lat": "4.87118172096886", 
       "lon": "52.2010877834008", 
       "name": "mijdrecht, Mijdrecht, Dr.Schaepmanplantsoen", 
       "id": "58542360"
     }, 
     {
       "lat": "4.87338374885194", 
       "lon": "52.1991379986487", 
       "name": "wilnis, Wilnis, Driehuis Kerk", 
       "id": "58542380"
     }, 
     {
       "lat": "4.91977634709483", 
       "lon": "52.2107724581436", 
       "name": "vinkeveen, Vinkeveen, Waverbancken", 
       "id": "58552030"
     }, 
     {
       "lat": "4.92237043853263", 
       "lon": "52.2117533970135", 
       "name": "vinkeveen, Vinkeveen, Hoge Biezenpad", 
       "id": "58552050"
     }, 
     {
       "lat": "4.92658024018619", 
       "lon": "52.213558495368", 
       "name": "vinkeveen, Vinkeveen, Winkelcentrum", 
       "id": "58552070"
     }, 
     {
       "lat": "4.93352985113183", 
       "lon": "52.215050431057", 
       "name": "vinkeveen, Vinkeveen, Kerklaan", 
       "id": "58552090"
     }, 
     {
       "lat": "4.93398500649144", 
       "lon": "52.2177755283852", 
       "name": "vinkeveen, Vinkeveen, Viadukt", 
       "id": "58552110"
     }, 
     {
       "lat": "5.25677478328973", 
       "lon": "52.364200796729", 
       "name": "almere stad, Almere Stad, Danswijk", 
       "id": "58650010"
     }, 
     {
       "lat": "5.25649723932566", 
       "lon": "52.3637241487222", 
       "name": "almere stad, Almere Stad, Danswijk", 
       "id": "58650020"
     }, 
     {
       "lat": "5.17596294333659", 
       "lon": "52.3498838255961", 
       "name": "almere stad, Almere Stad, Gooisepoort", 
       "id": "58650030"
     }, 
     {
       "lat": "5.1854125287258", 
       "lon": "52.3762070233564", 
       "name": "almere stad, Almere Stad, Fugaplantsoen", 
       "id": "58650040"
     }, 
     {
       "lat": "5.20655421391718", 
       "lon": "52.3594703010323", 
       "name": "almere stad, Almere Stad, Stedenwijk-Zuid", 
       "id": "58650050"
     }, 
     {
       "lat": "5.1787279938141", 
       "lon": "52.370524281272", 
       "name": "almere stad, Almere Stad, Wim Kanplein", 
       "id": "58650060"
     }, 
     {
       "lat": "5.17913655901435", 
       "lon": "52.3710732427189", 
       "name": "almere stad, Almere Stad, Wim Kanplein", 
       "id": "58650070"
     }, 
     {
       "lat": "5.18110700646199", 
       "lon": "52.3673018976462", 
       "name": "almere stad, Almere Stad, Count Basiestraat", 
       "id": "58650080"
     }, 
     {
       "lat": "5.18016612061566", 
       "lon": "52.3675608971909", 
       "name": "almere stad, Almere Stad, Count Basiestraat", 
       "id": "58650090"
     }, 
     {
       "lat": "5.1943569720857", 
       "lon": "52.3692116042073", 
       "name": "almere stad, Almere Stad, Componistenpad", 
       "id": "58650110"
     }, 
     {
       "lat": "5.19511959285823", 
       "lon": "52.3694195578172", 
       "name": "almere stad, Almere Stad, Componistenpad", 
       "id": "58650120"
     }, 
     {
       "lat": "5.23324273219576", 
       "lon": "52.3889512864964", 
       "name": "almere stad, Almere Stad, Waterwijk-Oost", 
       "id": "58650130"
     }, 
     {
       "lat": "5.18229775265928", 
       "lon": "52.3510813233481", 
       "name": "almere stad, Almere Stad, Gooisekant-West", 
       "id": "58650140"
     }, 
     {
       "lat": "5.20903982293326", 
       "lon": "52.3656125965665", 
       "name": "almere stad, Almere Stad, Stedenwijk-Midden", 
       "id": "58650150"
     }, 
     {
       "lat": "5.20192902108065", 
       "lon": "52.3562006543141", 
       "name": "almere stad, Almere Stad, Spanningsveld", 
       "id": "58650160"
     }, 
     {
       "lat": "5.20106196136244", 
       "lon": "52.3564419603835", 
       "name": "almere stad, Almere Stad, Spanningsveld", 
       "id": "58650170"
     }, 
     {
       "lat": "5.20609628152026", 
       "lon": "52.360170634995", 
       "name": "almere stad, Almere Stad, Stedenwijk-Zuid", 
       "id": "58650200"
     }, 
     {
       "lat": "5.19874028798627", 
       "lon": "52.367385189935", 
       "name": "almere stad, Almere Stad, Haydnplantsoen", 
       "id": "58650250"
     }, 
     {
       "lat": "5.19951967049552", 
       "lon": "52.367098824309", 
       "name": "almere stad, Almere Stad, Haydnplantsoen", 
       "id": "58650260"
     }, 
     {
       "lat": "5.19775069627273", 
       "lon": "52.3825186961215", 
       "name": "almere stad, Almere Stad, Kruidenwijk-West", 
       "id": "58650270"
     }, 
     {
       "lat": "5.19685557481331", 
       "lon": "52.3823285226347", 
       "name": "almere stad, Almere Stad, Kruidenwijk-West", 
       "id": "58650280"
     }, 
     {
       "lat": "5.18627798461523", 
       "lon": "52.3764241962367", 
       "name": "almere stad, Almere Stad, Fugaplantsoen", 
       "id": "58650290"
     }, 
     {
       "lat": "5.20966840892523", 
       "lon": "52.3662965973807", 
       "name": "almere stad, Almere Stad, Stedenwijk-Midden", 
       "id": "58650300"
     }, 
     {
       "lat": "5.20703937512534", 
       "lon": "52.3809963096591", 
       "name": "almere stad, Almere Stad, Kruidenwijk-Oost", 
       "id": "58650310"
     }, 
     {
       "lat": "5.20608362615452", 
       "lon": "52.3812644796161", 
       "name": "almere stad, Almere Stad, Kruidenwijk-Oost", 
       "id": "58650320"
     }, 
     {
       "lat": "5.23165831023954", 
       "lon": "52.3716032207522", 
       "name": "almere stad, Almere Stad, Greta Garboplantsoen", 
       "id": "58650330"
     }, 
     {
       "lat": "5.22996916365919", 
       "lon": "52.3717447926075", 
       "name": "almere stad, Almere Stad, Greta Garboplantsoen", 
       "id": "58650340"
     }, 
     {
       "lat": "5.21523414343563", 
       "lon": "52.3697740166955", 
       "name": "almere stad, Almere Stad, Passage", 
       "id": "58650350"
     }, 
     {
       "lat": "5.2161736596851", 
       "lon": "52.3698293021968", 
       "name": "almere stad, Almere Stad, Passage", 
       "id": "58650360"
     }, 
     {
       "lat": "5.22236733760485", 
       "lon": "52.3705481002554", 
       "name": "almere stad, Almere Stad, Flevoziekenhuis", 
       "id": "58650370"
     }, 
     {
       "lat": "5.22201486796532", 
       "lon": "52.3705655845308", 
       "name": "almere stad, Almere Stad, Flevoziekenhuis", 
       "id": "58650380"
     }, 
     {
       "lat": "5.21954345051982", 
       "lon": "52.3834413031387", 
       "name": "almere stad, Almere Stad, Markerkant", 
       "id": "58650410"
     }, 
     {
       "lat": "5.21998188043438", 
       "lon": "52.3840261139596", 
       "name": "almere stad, Almere Stad, Markerkant", 
       "id": "58650420"
     }, 
     {
       "lat": "5.22578855149424", 
       "lon": "52.386712456609", 
       "name": "almere stad, Almere Stad, Waterwijk-West", 
       "id": "58650450"
     }, 
     {
       "lat": "5.22681592315708", 
       "lon": "52.3869475277575", 
       "name": "almere stad, Almere Stad, Waterwijk-West", 
       "id": "58650460"
     }, 
     {
       "lat": "5.23422612645261", 
       "lon": "52.3891862360184", 
       "name": "almere stad, Almere Stad, Waterwijk-Oost", 
       "id": "58650490"
     }, 
     {
       "lat": "5.24314340884332", 
       "lon": "52.3799402294452", 
       "name": "almere stad, Almere Stad, Verzetswijk", 
       "id": "58650500"
     }, 
     {
       "lat": "5.24295490784978", 
       "lon": "52.3791940324793", 
       "name": "almere stad, Almere Stad, Verzetswijk", 
       "id": "58650510"
     }, 
     {
       "lat": "5.25287177016196", 
       "lon": "52.368312750529", 
       "name": "almere stad, Almere Stad, Parkwijk-Zuid", 
       "id": "58650520"
     }, 
     {
       "lat": "5.24528468649357", 
       "lon": "52.376275886407", 
       "name": "almere stad, Almere Stad, Station Parkwijk", 
       "id": "58650530"
     }, 
     {
       "lat": "5.24503201290057", 
       "lon": "52.37721927813", 
       "name": "almere stad, Almere Stad, Station Parkwijk", 
       "id": "58650540"
     }, 
     {
       "lat": "5.25267953328224", 
       "lon": "52.3687619115144", 
       "name": "almere stad, Almere Stad, Parkwijk-Zuid", 
       "id": "58650550"
     }, 
     {
       "lat": "5.24764211440936", 
       "lon": "52.3738071042034", 
       "name": "almere stad, Almere Stad, Parkwijk-Midden", 
       "id": "58650570"
     }, 
     {
       "lat": "5.24881805442959", 
       "lon": "52.3734310051463", 
       "name": "almere stad, Almere Stad, Parkwijk-Midden", 
       "id": "58650580"
     }, 
     {
       "lat": "5.23842843297124", 
       "lon": "52.3669653344134", 
       "name": "almere stad, Almere Stad, Romy Schneiderweg", 
       "id": "58650590"
     }, 
     {
       "lat": "5.23795648547956", 
       "lon": "52.3675938718993", 
       "name": "almere stad, Almere Stad, Romy Schneiderweg", 
       "id": "58650600"
     }, 
     {
       "lat": "5.24192068881379", 
       "lon": "52.3631319672189", 
       "name": "almere stad, Almere Stad, Bunuellaan", 
       "id": "58650610"
     }, 
     {
       "lat": "5.24158122781666", 
       "lon": "52.3636797936178", 
       "name": "almere stad, Almere Stad, Bunuellaan", 
       "id": "58650620"
     }, 
     {
       "lat": "5.24291344612157", 
       "lon": "52.3919473175715", 
       "name": "almere buiten, Almere Buiten, FBK-Sportpark", 
       "id": "58650630"
     }, 
     {
       "lat": "5.2444245220835", 
       "lon": "52.3606274720145", 
       "name": "almere stad, Almere Stad, Walt Disneyplantsoen", 
       "id": "58650640"
     }, 
     {
       "lat": "5.24554110427294", 
       "lon": "52.360350196804", 
       "name": "almere stad, Almere Stad, Walt Disneyplantsoen", 
       "id": "58650650"
     }, 
     {
       "lat": "5.25254662410649", 
       "lon": "52.3835373209877", 
       "name": "almere stad, Almere Stad, Tussen de Vaarten-N", 
       "id": "58650710"
     }, 
     {
       "lat": "5.25389665695551", 
       "lon": "52.3839522743973", 
       "name": "almere stad, Almere Stad, Tussen de Vaarten-N", 
       "id": "58650740"
     }, 
     {
       "lat": "5.18141817522304", 
       "lon": "52.3508551074694", 
       "name": "almere stad, Almere Stad, Gooisekant-West", 
       "id": "58650790"
     }, 
     {
       "lat": "5.17622848812303", 
       "lon": "52.3495966948095", 
       "name": "almere stad, Almere Stad, Gooisepoort", 
       "id": "58650820"
     }, 
     {
       "lat": "5.27456081926809", 
       "lon": "52.3962327123459", 
       "name": "almere buiten, Almere Buiten, Noordeinde", 
       "id": "58750020"
     }, 
     {
       "lat": "5.28284960951937", 
       "lon": "52.3889244440651", 
       "name": "almere buiten, Almere Buiten, Bloemenbuurt", 
       "id": "58750030"
     }, 
     {
       "lat": "5.28311258863056", 
       "lon": "52.3895358278279", 
       "name": "almere buiten, Almere Buiten, Bloemenbuurt", 
       "id": "58750040"
     }, 
     {
       "lat": "5.26497320844497", 
       "lon": "52.3886197622174", 
       "name": "almere buiten, Almere Buiten, Landgoederenbuurt", 
       "id": "58750180"
     }, 
     {
       "lat": "5.26426876180746", 
       "lon": "52.3883853577455", 
       "name": "almere buiten, Almere Buiten, Landgoederenbuurt", 
       "id": "58750190"
     }, 
     {
       "lat": "5.27364803035221", 
       "lon": "52.3969688189484", 
       "name": "almere buiten, Almere Buiten, Molenbuurt-Zuid", 
       "id": "58750210"
     }, 
     {
       "lat": "5.27311765441673", 
       "lon": "52.3975345239733", 
       "name": "almere buiten, Almere Buiten, Molenbuurt-Zuid", 
       "id": "58750220"
     }, 
     {
       "lat": "5.24391286790922", 
       "lon": "52.3918047292424", 
       "name": "almere buiten, Almere Buiten, FBK-Sportpark", 
       "id": "58750230"
     }, 
     {
       "lat": "5.26880349591049", 
       "lon": "52.4010084659977", 
       "name": "almere buiten, Almere Buiten, Molenbuurt-Noord", 
       "id": "58750250"
     }, 
     {
       "lat": "5.27297253213794", 
       "lon": "52.3854191858181", 
       "name": "almere buiten, Almere Buiten, Faunabuurt", 
       "id": "58750260"
     }, 
     {
       "lat": "5.27214974882372", 
       "lon": "52.385508265711", 
       "name": "almere buiten, Almere Buiten, Faunabuurt", 
       "id": "58750270"
     }, 
     {
       "lat": "5.25459654472625", 
       "lon": "52.3955020507589", 
       "name": "almere buiten, Almere Buiten, Bouwmeesterbuurt-W", 
       "id": "58750280"
     }, 
     {
       "lat": "5.25544778453443", 
       "lon": "52.3957995883214", 
       "name": "almere buiten, Almere Buiten, Bouwmeesterbuurt-W", 
       "id": "58750290"
     }, 
     {
       "lat": "5.26774509941251", 
       "lon": "52.4011781673953", 
       "name": "almere buiten, Almere Buiten, Molenbuurt-Noord", 
       "id": "58750300"
     }, 
     {
       "lat": "5.26147869244682", 
       "lon": "52.3984304948087", 
       "name": "almere buiten, Almere Buiten, Bouwmeesterbuurt-O", 
       "id": "58750310"
     }, 
     {
       "lat": "5.26036325434764", 
       "lon": "52.3980068931427", 
       "name": "almere buiten, Almere Buiten, Bouwmeesterbuurt-O", 
       "id": "58750320"
     }, 
     {
       "lat": "5.26784609298599", 
       "lon": "52.4018703079765", 
       "name": "almere buiten, Almere Buiten, Molenbuurt-Noord", 
       "id": "58750410"
     }, 
     {
       "lat": "4.90536453001731", 
       "lon": "52.2013220942917", 
       "name": "wilnis, Wilnis, Begraafplaats", 
       "id": "59542000"
     }, 
     {
       "lat": "4.87388539655336", 
       "lon": "52.1987626838391", 
       "name": "wilnis, Wilnis, Driehuis Kerk", 
       "id": "59542010"
     }, 
     {
       "lat": "4.88402105275845", 
       "lon": "52.1962537159579", 
       "name": "wilnis, Wilnis, Veldzijdeweg", 
       "id": "59542020"
     }, 
     {
       "lat": "4.88427161393065", 
       "lon": "52.1960840112135", 
       "name": "wilnis, Wilnis, Veldzijdeweg", 
       "id": "59542030"
     }, 
     {
       "lat": "4.89150299015756", 
       "lon": "52.1942271092571", 
       "name": "wilnis, Wilnis, Burg. Padmosweg", 
       "id": "59542040"
     }, 
     {
       "lat": "4.89179778553788", 
       "lon": "52.1940216222436", 
       "name": "wilnis, Wilnis, Burg. Padmosweg", 
       "id": "59542050"
     }, 
     {
       "lat": "4.90536453001731", 
       "lon": "52.2013220942917", 
       "name": "wilnis, Wilnis, Begraafplaats", 
       "id": "59542090"
     }, 
     {
       "lat": "4.89715385567369", 
       "lon": "52.1950686071062", 
       "name": "wilnis, Wilnis, Herenweg", 
       "id": "59542130"
     }, 
     {
       "lat": "4.89688832857993", 
       "lon": "52.1952742289522", 
       "name": "wilnis, Wilnis, Herenweg", 
       "id": "59542140"
     }, 
     {
       "lat": "4.8961738964834", 
       "lon": "52.1990552103761", 
       "name": "wilnis, Wilnis, Molmlaan", 
       "id": "59542150"
     }, 
     {
       "lat": "4.89600243795169", 
       "lon": "52.1986859891241", 
       "name": "wilnis, Wilnis, Molmlaan", 
       "id": "59542160"
     }, 
     {
       "lat": "4.9015213730826", 
       "lon": "52.2009558180746", 
       "name": "wilnis, Wilnis, Burg. de Voogtlaan", 
       "id": "59542170"
     }, 
     {
       "lat": "4.90023310306218", 
       "lon": "52.2010493803213", 
       "name": "wilnis, Wilnis, Burg. de Voogtlaan", 
       "id": "59542200"
     }, 
     {
       "lat": "4.46418369954161", 
       "lon": "52.1798486915113", 
       "name": "oegstgeest, Oegstgeest, Leidsebuurt", 
       "id": "54550630"
     }, 
     {
       "lat": "4.45942945265581", 
       "lon": "52.2361774041289", 
       "name": "noordwijk, Noordwijk, Boechorst", 
       "id": "54660520"
     }, 
     {
       "lat": "4.45841177254736", 
       "lon": "52.2365379275789", 
       "name": "noordwijk, Noordwijk, Boechorst", 
       "id": "54660590"
     }, 
     {
       "lat": "4.63824690989142", 
       "lon": "52.3871686433413", 
       "name": "haarlem, Haarlem, Station NS", 
       "id": "55000051"
     }, 
     {
       "lat": "4.6434428918756", 
       "lon": "52.3050875615983", 
       "name": "hoofddorp, Hoofddorp, F. Blankers-Koenlaan", 
       "id": "56230210"
     }, 
     {
       "lat": "4.6431469662661", 
       "lon": "52.3052474843787", 
       "name": "hoofddorp, Hoofddorp, F. Blankers-Koenlaan", 
       "id": "56230220"
     }, 
     {
       "lat": "4.6381073891917", 
       "lon": "52.3015126054853", 
       "name": "hoofddorp, Hoofddorp, Pagode", 
       "id": "56230230"
     }, 
     {
       "lat": "4.63695762016271", 
       "lon": "52.3010109752015", 
       "name": "hoofddorp, Hoofddorp, Pagode", 
       "id": "56230240"
     }, 
     {
       "lat": "4.63242834269943", 
       "lon": "52.3061322921006", 
       "name": "hoofddorp, Hoofddorp, Duinbeek", 
       "id": "56230250"
     }, 
     {
       "lat": "4.68007586492916", 
       "lon": "52.3056088761611", 
       "name": "hoofddorp, Hoofddorp, Wilsonstraat", 
       "id": "56332350"
     }, 
     {
       "lat": "4.67993611932354", 
       "lon": "52.3051766174149", 
       "name": "hoofddorp, Hoofddorp, Wilsonstraat", 
       "id": "56332360"
     }, 
     {
       "lat": "4.68161370981104", 
       "lon": "52.3094109871421", 
       "name": "hoofddorp, Hoofddorp, Kaj Munkweg", 
       "id": "56333010"
     }, 
     {
       "lat": "4.68180489147563", 
       "lon": "52.3093761756461", 
       "name": "hoofddorp, Hoofddorp, Kaj Munkweg", 
       "id": "56333020"
     }, 
     {
       "lat": "4.87714082466593", 
       "lon": "52.3692677503546", 
       "name": "amsterdam, Amsterdam, Marnixstraat", 
       "id": "57000072"
     }, 
     {
       "lat": "4.86925774626037", 
       "lon": "52.3250856052545", 
       "name": "amsterdam, Amsterdam, van Boshuizenstraat", 
       "id": "57142140"
     }, 
     {
       "lat": "4.76958713544693", 
       "lon": "52.3501327823408", 
       "name": "lijnden, Lijnden, Akerdijk 90", 
       "id": "57230010"
     }, 
     {
       "lat": "4.76947060267172", 
       "lon": "52.35006925935", 
       "name": "lijnden, Lijnden, Akerdijk 90", 
       "id": "57230020"
     }, 
     {
       "lat": "4.77659783028064", 
       "lon": "52.3472930537009", 
       "name": "badhoevedorp, Badhoevedorp, Akerdijk 169", 
       "id": "57230030"
     }, 
     {
       "lat": "4.77687742644768", 
       "lon": "52.3419017941856", 
       "name": "badhoevedorp, Badhoevedorp, Einsteinlaan", 
       "id": "57230060"
     }, 
     {
       "lat": "4.77735831337474", 
       "lon": "52.3421469450382", 
       "name": "badhoevedorp, Badhoevedorp, Einsteinlaan", 
       "id": "57230070"
     }, 
     {
       "lat": "4.77651076873877", 
       "lon": "52.3472207018344", 
       "name": "badhoevedorp, Badhoevedorp, Akerdijk 169", 
       "id": "57230100"
     }, 
     {
       "lat": "4.77933845241835", 
       "lon": "52.3454287050413", 
       "name": "badhoevedorp, Badhoevedorp, Geraniumlaan", 
       "id": "57230110"
     }, 
     {
       "lat": "4.77942822224454", 
       "lon": "52.3453033364334", 
       "name": "badhoevedorp, Badhoevedorp, Geraniumlaan", 
       "id": "57230120"
     }, 
     {
       "lat": "4.80232269328207", 
       "lon": "52.3329975199105", 
       "name": "badhoevedorp, Badhoevedorp, Viaduct A4", 
       "id": "57230130"
     }, 
     {
       "lat": "4.80270483489697", 
       "lon": "52.3329454812042", 
       "name": "badhoevedorp, Badhoevedorp, Viaduct A4", 
       "id": "57230140"
     }, 
     {
       "lat": "4.80792830354235", 
       "lon": "52.3306612947797", 
       "name": "badhoevedorp, Badhoevedorp, Nieuwemeerdijk 242", 
       "id": "57230150"
     }, 
     {
       "lat": "4.80823671864339", 
       "lon": "52.3306358408101", 
       "name": "badhoevedorp, Badhoevedorp, Nieuwemeerdijk 242", 
       "id": "57230160"
     }, 
     {
       "lat": "4.81492019516512", 
       "lon": "52.3277113575095", 
       "name": "badhoevedorp, Badhoevedorp, Koekoekslaan", 
       "id": "57230170"
     }, 
     {
       "lat": "4.8151843481466", 
       "lon": "52.3277036470693", 
       "name": "badhoevedorp, Badhoevedorp, Koekoekslaan", 
       "id": "57230180"
     }, 
     {
       "lat": "4.81764573876962", 
       "lon": "52.3210824933638", 
       "name": "badhoevedorp, Badhoevedorp, Nieuwemeerdijk 406", 
       "id": "57230190"
     }, 
     {
       "lat": "4.8177784289532", 
       "lon": "52.3210292050212", 
       "name": "badhoevedorp, Badhoevedorp, Nieuwemeerdijk 406", 
       "id": "57230200"
     }, 
     {
       "lat": "4.80253423981598", 
       "lon": "52.3291877204931", 
       "name": "ONBEKEND, Nieuwe Meer, Koekoekslaan", 
       "id": "57232100"
     }, 
     {
       "lat": "4.80279804882895", 
       "lon": "52.3292069995145", 
       "name": "ONBEKEND, Nieuwe Meer, Koekoekslaan", 
       "id": "57232160"
     }, 
     {
       "lat": "4.79735798126653", 
       "lon": "52.3345367592318", 
       "name": "badhoevedorp, Badhoevedorp, Meidoornweg", 
       "id": "57232340"
     }, 
     {
       "lat": "4.7974623490143", 
       "lon": "52.3344114496963", 
       "name": "badhoevedorp, Badhoevedorp, Meidoornweg", 
       "id": "57232350"
     }, 
     {
       "lat": "4.76175135405023", 
       "lon": "52.3531295210723", 
       "name": "lijnden, Lijnden, Lijnderdijk (Gemaal)", 
       "id": "57232470"
     }, 
     {
       "lat": "4.76195581939813", 
       "lon": "52.3532025040155", 
       "name": "lijnden, Lijnden, Lijnderdijk (Gemaal)", 
       "id": "57232480"
     }, 
     {
       "lat": "4.79143875875479", 
       "lon": "52.3339228945863", 
       "name": "badhoevedorp, Badhoevedorp, Haamstedestraat", 
       "id": "57232700"
     }, 
     {
       "lat": "4.79158522502755", 
       "lon": "52.3339416076393", 
       "name": "badhoevedorp, Badhoevedorp, Haamstedestraat", 
       "id": "57232710"
     }, 
     {
       "lat": "4.79593841811263", 
       "lon": "52.3331635224316", 
       "name": "badhoevedorp, Badhoevedorp, Egelantierstraat", 
       "id": "57232720"
     }, 
     {
       "lat": "4.79605398743461", 
       "lon": "52.3332989175134", 
       "name": "badhoevedorp, Badhoevedorp, Egelantierstraat", 
       "id": "57232730"
     }, 
     {
       "lat": "4.8558815414352", 
       "lon": "52.2795657146301", 
       "name": "amstelveen, Amstelveen, Praam", 
       "id": "57242500"
     }, 
     {
       "lat": "4.85626198122343", 
       "lon": "52.2796123632154", 
       "name": "amstelveen, Amstelveen, Praam", 
       "id": "57242900"
     }, 
     {
       "lat": "4.8539747140648", 
       "lon": "52.2870530301636", 
       "name": "amstelveen, Amstelveen, Startbaan", 
       "id": "57243131"
     }, 
     {
       "lat": "4.85411865948215", 
       "lon": "52.2774905624038", 
       "name": "amstelveen, Amstelveen, Jupiter", 
       "id": "57243660"
     }, 
     {
       "lat": "4.85466597577057", 
       "lon": "52.2782839641563", 
       "name": "amstelveen, Amstelveen, Jupiter", 
       "id": "57243670"
     }, 
     {
       "lat": "4.86335385788188", 
       "lon": "52.308270352013", 
       "name": "amstelveen, Amstelveen, Graaf Aelbrechtlaan", 
       "id": "57244020"
     }, 
     {
       "lat": "4.86335385788188", 
       "lon": "52.308270352013", 
       "name": "amstelveen, Amstelveen, Graaf Aelbrechtlaan", 
       "id": "57244021"
     }, 
     {
       "lat": "4.94741598475706", 
       "lon": "52.3113989805315", 
       "name": "amsterdam-zo, Amsterdam-ZO, Bijlmer ArenA", 
       "id": "57250510"
     }, 
     {
       "lat": "4.94741598475706", 
       "lon": "52.3113989805315", 
       "name": "amsterdam-zo, Amsterdam-ZO, Bijlmer ArenA", 
       "id": "57250570"
     }, 
     {
       "lat": "4.9476837516749", 
       "lon": "52.3110135008347", 
       "name": "amsterdam-zo, Amsterdam-ZO, Bijlmer ArenA", 
       "id": "57250580"
     }, 
     {
       "lat": "4.94762429770732", 
       "lon": "52.311094170013", 
       "name": "amsterdam-zo, Amsterdam-ZO, Bijlmer ArenA", 
       "id": "57250590"
     }, 
     {
       "lat": "4.79958202623822", 
       "lon": "52.3228007074839", 
       "name": "ONBEKEND, Schiphol Noord, Cateringweg", 
       "id": "57330140"
     }, 
     {
       "lat": "4.79955257317944", 
       "lon": "52.3228095490448", 
       "name": "ONBEKEND, Schiphol Noord, Cateringweg", 
       "id": "57330150"
     }, 
     {
       "lat": "4.79620712608149", 
       "lon": "52.3206897241443", 
       "name": "ONBEKEND, Schiphol Noord, Loevesteinse Dwarsw.", 
       "id": "57330280"
     }, 
     {
       "lat": "4.80904089392738", 
       "lon": "52.3083049469364", 
       "name": "schiphol oost, Schiphol Oost, Stationsplein", 
       "id": "57340333"
     }, 
     {
       "lat": "4.81026564432445", 
       "lon": "52.3088412120449", 
       "name": "schiphol oost, Schiphol Oost, Stationsplein", 
       "id": "57340570"
     }, 
     {
       "lat": "4.75039171581535", 
       "lon": "52.2865405160725", 
       "name": "ONBEKEND, Schiphol-ZO, Folkstoneweg", 
       "id": "57342440"
     }, 
     {
       "lat": "4.75078868731094", 
       "lon": "52.2864527739501", 
       "name": "ONBEKEND, Schiphol-ZO, Folkstoneweg", 
       "id": "57342450"
     }, 
     {
       "lat": "4.75943792600558", 
       "lon": "52.290453710414", 
       "name": "ONBEKEND, Schiphol-ZO, Oude Meerweg", 
       "id": "57342480"
     }, 
     {
       "lat": "4.75999473931217", 
       "lon": "52.2904656532747", 
       "name": "ONBEKEND, Schiphol-ZO, Oude Meerweg", 
       "id": "57342490"
     }, 
     {
       "lat": "4.76855266593146", 
       "lon": "52.2906096061245", 
       "name": "ONBEKEND, Schiphol-ZO, P80 Parkeerterrein", 
       "id": "57342500"
     }, 
     {
       "lat": "4.76853951022696", 
       "lon": "52.2905016820538", 
       "name": "ONBEKEND, Schiphol-ZO, P80 Parkeerterrein", 
       "id": "57342520"
     }, 
     {
       "lat": "4.76829443059015", 
       "lon": "52.2944191384876", 
       "name": "ONBEKEND, Schiphol-ZO, Ganderweg", 
       "id": "57342550"
     }, 
     {
       "lat": "4.91888988007645", 
       "lon": "52.2965045309177", 
       "name": "ouderkerk a/d amstel, Ouderkerk a/d Amstel, Hoofdenburg", 
       "id": "58252510"
     }, 
     {
       "lat": "4.91919771130734", 
       "lon": "52.2965057494908", 
       "name": "ouderkerk a/d amstel, Ouderkerk a/d Amstel, Hoofdenburg", 
       "id": "58252520"
     }, 
     {
       "lat": "4.81366935163378", 
       "lon": "52.4313519933257", 
       "name": "zaandam, Zaandam, Albert Heijnweg", 
       "id": "37220580"
     }, 
     {
       "lat": "4.78700591973983", 
       "lon": "52.4295572359706", 
       "name": "zaandam, Zaandam, Willem Hooftkade", 
       "id": "37222030"
     }, 
     {
       "lat": "4.79635755132141", 
       "lon": "52.4284358333827", 
       "name": "zaandam, Zaandam, Schellingweg", 
       "id": "37222050"
     }, 
     {
       "lat": "4.79815586533319", 
       "lon": "52.4280942668453", 
       "name": "zaandam, Zaandam, Schellingweg", 
       "id": "37222060"
     }, 
     {
       "lat": "4.77312573847959", 
       "lon": "52.4316881055989", 
       "name": "westzaan, Westzaan, Kleine Steng", 
       "id": "37222070"
     }, 
     {
       "lat": "4.77371685060407", 
       "lon": "52.4314754627994", 
       "name": "westzaan, Westzaan, Kleine Steng", 
       "id": "37222080"
     }, 
     {
       "lat": "4.78840617347757", 
       "lon": "52.4293036770793", 
       "name": "zaandam, Zaandam, Willem Hooftkade", 
       "id": "37222160"
     }, 
     {
       "lat": "4.80186761954573", 
       "lon": "52.4287058445696", 
       "name": "zaandam, Zaandam, Ducaatstraat", 
       "id": "37225000"
     }, 
     {
       "lat": "4.81172832853654", 
       "lon": "52.4302281148801", 
       "name": "zaandam, Zaandam, Ronde Tocht", 
       "id": "37225010"
     }, 
     {
       "lat": "4.81135155199561", 
       "lon": "52.4298038648951", 
       "name": "zaandam, Zaandam, Ronde Tocht", 
       "id": "37225020"
     }, 
     {
       "lat": "4.80734458543343", 
       "lon": "52.4292630423639", 
       "name": "zaandam, Zaandam, Grote Tocht", 
       "id": "37225030"
     }, 
     {
       "lat": "4.80900724291792", 
       "lon": "52.4291723019203", 
       "name": "zaandam, Zaandam, Grote Tocht", 
       "id": "37225040"
     }, 
     {
       "lat": "4.80275295193495", 
       "lon": "52.4284675472919", 
       "name": "zaandam, Zaandam, Ducaatstraat", 
       "id": "37225050"
     }, 
     {
       "lat": "4.68346575492035", 
       "lon": "52.4525713954421", 
       "name": "assendelft, Assendelft, Vuurlinie", 
       "id": "37330010"
     }, 
     {
       "lat": "4.72622176348532", 
       "lon": "52.435471260562", 
       "name": "nauerna, Nauerna, Pont Buitenhuizen", 
       "id": "37330350"
     }, 
     {
       "lat": "4.72629260131205", 
       "lon": "52.4356514097681", 
       "name": "nauerna, Nauerna, Pont Buitenhuizen", 
       "id": "37330360"
     }, 
     {
       "lat": "4.6861931490488", 
       "lon": "52.4512753498138", 
       "name": "assendelft, Assendelft, Vuurlinie", 
       "id": "37430020"
     }, 
     {
       "lat": "4.66912087060351", 
       "lon": "52.4680700527361", 
       "name": "beverwijk, Beverwijk, Beveland", 
       "id": "37436000"
     }, 
     {
       "lat": "4.6709946786802", 
       "lon": "52.471406830099", 
       "name": "beverwijk, Beverwijk, Salland", 
       "id": "56300440"
     }, 
     {
       "lat": "4.66881874661931", 
       "lon": "52.4667380440074", 
       "name": "beverwijk, Beverwijk, Beveland", 
       "id": "56300450"
     }, 
     {
       "lat": "4.67101434324765", 
       "lon": "52.4711013676046", 
       "name": "beverwijk, Beverwijk, Salland", 
       "id": "56300500"
     }, 
     {
       "lat": "4.66524913169182", 
       "lon": "52.4780678116053", 
       "name": "beverwijk, Beverwijk, Wijkermeerweg", 
       "id": "56302010"
     }, 
     {
       "lat": "4.65412528468015", 
       "lon": "52.477810829132", 
       "name": "beverwijk, Beverwijk, Station NS", 
       "id": "56302551"
     }, 
     {
       "lat": "4.67084129512656", 
       "lon": "52.4745156412335", 
       "name": "beverwijk, Beverwijk, Randweg", 
       "id": "56303020"
     }, 
     {
       "lat": "4.66453119828974", 
       "lon": "52.4787644775543", 
       "name": "beverwijk, Beverwijk, Wijkermeerweg", 
       "id": "56303040"
     }, 
     {
       "lat": "4.6713632308801", 
       "lon": "52.4740963721909", 
       "name": "beverwijk, Beverwijk, Randweg", 
       "id": "56303050"
     }, 
     {
       "lat": "4.85775829380766", 
       "lon": "52.2794752671494", 
       "name": "amstelveen, Amstelveen, Goedereede", 
       "id": "57240100"
     }, 
     {
       "lat": "4.85753924943638", 
       "lon": "52.279411370762", 
       "name": "amstelveen, Amstelveen, Goedereede", 
       "id": "57240110"
     }, 
     {
       "lat": "4.86175938801667", 
       "lon": "52.2794212139726", 
       "name": "amstelveen, Amstelveen, Winkelc. Waardhuizen", 
       "id": "57240120"
     }, 
     {
       "lat": "4.86158153528949", 
       "lon": "52.2795911933424", 
       "name": "amstelveen, Amstelveen, Winkelc. Waardhuizen", 
       "id": "57240130"
     }, 
     {
       "lat": "4.84802744430992", 
       "lon": "52.2964633338199", 
       "name": "amstelveen, Amstelveen, Populierenlaan", 
       "id": "57242730"
     }, 
     {
       "lat": "4.87403526272154", 
       "lon": "52.3407092295944", 
       "name": "amsterdam, Amsterdam, Station Zuid", 
       "id": "57142235"
     }, 
     {
       "lat": "4.75760542099474", 
       "lon": "52.2625273368483", 
       "name": "aalsmeer, Aalsmeer, Hortensiaplein", 
       "id": "57442665"
     }, 
     {
       "lat": "4.7577192922404", 
       "lon": "52.2627616311768", 
       "name": "aalsmeer, Aalsmeer, Hortensiaplein", 
       "id": "57442666"
     }, 
     {
       "lat": "4.83714278204202", 
       "lon": "52.2745546401587", 
       "name": "amstelveen, Amstelveen, Burg. Wiegelweg", 
       "id": "57243840"
     }, 
     {
       "lat": "4.76716475710034", 
       "lon": "52.258748990404", 
       "name": "aalsmeer, Aalsmeer, Zwarteweg/N201", 
       "id": "57440010"
     }, 
     {
       "lat": "4.83781107892941", 
       "lon": "52.2738297266577", 
       "name": "amstelveen, Amstelveen, Burg. Wiegelweg", 
       "id": "58342020"
     }, 
     {
       "lat": "4.65715313205312", 
       "lon": "52.2952142762425", 
       "name": "hoofddorp, Hoofddorp, Toolenburg Zuid", 
       "id": "56330020"
     }, 
     {
       "lat": "4.65771976543989", 
       "lon": "52.2955233659142", 
       "name": "hoofddorp, Hoofddorp, Toolenburg Zuid", 
       "id": "56330030"
     }, 
     {
       "lat": "4.73378882999864", 
       "lon": "52.2843737043204", 
       "name": "rozenburg, Rozenburg, van Zanten", 
       "id": "57343210"
     }, 
     {
       "lat": "4.73410000122437", 
       "lon": "52.2841417363577", 
       "name": "rozenburg, Rozenburg, van Zanten", 
       "id": "57343220"
     }, 
     {
       "lat": "4.7392683586153", 
       "lon": "52.2834781002046", 
       "name": "rozenburg, Rozenburg, Aalsmeerderweg", 
       "id": "57343230"
     }, 
     {
       "lat": "4.74001125943609", 
       "lon": "52.2827811075718", 
       "name": "rozenburg, Rozenburg, Aalsmeerderweg", 
       "id": "57343240"
     }, 
     {
       "lat": "4.7461783730306", 
       "lon": "52.2799115927555", 
       "name": "schiphol-rijk, Schiphol-Rijk, Beechavenue", 
       "id": "57343250"
     }, 
     {
       "lat": "4.74676083339068", 
       "lon": "52.279150771992", 
       "name": "schiphol-rijk, Schiphol-Rijk, Beechavenue", 
       "id": "57343260"
     }, 
     {
       "lat": "4.91217292658803", 
       "lon": "52.4270602757138", 
       "name": "landsmeer, Landsmeer, Luyendijk", 
       "id": "37212840"
     }, 
     {
       "lat": "4.91340527475763", 
       "lon": "52.4286829759714", 
       "name": "landsmeer, Landsmeer, van Beekstraat", 
       "id": "37212860"
     }, 
     {
       "lat": "4.91852053213078", 
       "lon": "52.4329814063512", 
       "name": "landsmeer, Landsmeer, Fuutstraat", 
       "id": "37212940"
     }, 
     {
       "lat": "4.83450843961575", 
       "lon": "52.4263550186237", 
       "name": "zaandam, Zaandam, Delftse Rij", 
       "id": "37220030"
     }, 
     {
       "lat": "4.80256242748417", 
       "lon": "52.4584853088347", 
       "name": "koog a/d zaan, Koog a/d Zaan, Glazenmaker", 
       "id": "37220060"
     }, 
     {
       "lat": "4.8018229334816", 
       "lon": "52.4576637877146", 
       "name": "koog a/d zaan, Koog a/d Zaan, Glazenmaker", 
       "id": "37220061"
     }, 
     {
       "lat": "4.83163317763713", 
       "lon": "52.4293614223239", 
       "name": "zaandam, Zaandam, Zweedsestraat", 
       "id": "37220070"
     }, 
     {
       "lat": "4.7934544676589", 
       "lon": "52.4585299227204", 
       "name": "koog a/d zaan, Koog a/d Zaan, Gouwzoom", 
       "id": "37220080"
     }, 
     {
       "lat": "4.82941501974767", 
       "lon": "52.4303666064235", 
       "name": "zaandam, Zaandam, Rigastraat", 
       "id": "37220090"
     }, 
     {
       "lat": "4.82553166334421", 
       "lon": "52.431651473378", 
       "name": "zaandam, Zaandam, Archangelstraat", 
       "id": "37220110"
     }, 
     {
       "lat": "4.77166980439208", 
       "lon": "52.4655460083075", 
       "name": "westzaan, Westzaan, Kerkbuurt", 
       "id": "37220120"
     }, 
     {
       "lat": "4.78101981904225", 
       "lon": "52.4672748593308", 
       "name": "westzaan, Westzaan, Middel", 
       "id": "37220140"
     }, 
     {
       "lat": "4.8143246585302", 
       "lon": "52.4307080520161", 
       "name": "zaandam, Zaandam, Albert Heijnweg", 
       "id": "37220150"
     }, 
     {
       "lat": "4.81254308436756", 
       "lon": "52.4376918150063", 
       "name": "zaandam, Zaandam, Houtveldweg/NS", 
       "id": "37220170"
     }, 
     {
       "lat": "4.78153301281694", 
       "lon": "52.4308685545375", 
       "name": "westzaan, Westzaan, Overtoom/Zuideinde", 
       "id": "37220310"
     }, 
     {
       "lat": "4.78174131033884", 
       "lon": "52.4306898654355", 
       "name": "westzaan, Westzaan, Overtoom/Zuideinde", 
       "id": "37220420"
     }, 
     {
       "lat": "4.78124251309234", 
       "lon": "52.4671321958905", 
       "name": "westzaan, Westzaan, Middel", 
       "id": "37220590"
     }, 
     {
       "lat": "4.79315021062875", 
       "lon": "52.459274370437", 
       "name": "koog a/d zaan, Koog a/d Zaan, Gouwzoom", 
       "id": "37220650"
     }, 
     {
       "lat": "4.81198897653946", 
       "lon": "52.4497774869338", 
       "name": "zaandam, Zaandam, J. v. Goyenkade", 
       "id": "37220670"
     }, 
     {
       "lat": "4.81790710930693", 
       "lon": "52.4574185568902", 
       "name": "zaandam, Zaandam, Kogerveld NS", 
       "id": "37220680"
     }, 
     {
       "lat": "4.84232424717832", 
       "lon": "52.4710326131085", 
       "name": "zaandam, Zaandam, Schipbeek", 
       "id": "37220700"
     }, 
     {
       "lat": "4.8181391449011", 
       "lon": "52.4576803111548", 
       "name": "zaandam, Zaandam, Kogerveld NS", 
       "id": "37220710"
     }, 
     {
       "lat": "4.81827559612015", 
       "lon": "52.4573664001018", 
       "name": "zaandam, Zaandam, Kogerveld NS", 
       "id": "37220711"
     }, 
     {
       "lat": "4.83759933327083", 
       "lon": "52.4699053396107", 
       "name": "zaandam, Zaandam, Kennemerbeek", 
       "id": "37220720"
     }, 
     {
       "lat": "4.82152090053579", 
       "lon": "52.4543980460173", 
       "name": "zaandam, Zaandam, Hof van Zaenden", 
       "id": "37220730"
     }, 
     {
       "lat": "4.83489069121833", 
       "lon": "52.4687872848184", 
       "name": "zaandam, Zaandam, IJssel", 
       "id": "37220740"
     }, 
     {
       "lat": "4.81809691955065", 
       "lon": "52.4598191560935", 
       "name": "zaandam, Zaandam, Jufferstraat", 
       "id": "37220750"
     }, 
     {
       "lat": "4.83046889141134", 
       "lon": "52.4681644404532", 
       "name": "zaandam, Zaandam, De Twee Gebroeders", 
       "id": "37220760"
     }, 
     {
       "lat": "4.82281096526047", 
       "lon": "52.4651353767548", 
       "name": "zaandam, Zaandam, Sportvelden", 
       "id": "37220770"
     }, 
     {
       "lat": "4.82685196656843", 
       "lon": "52.466745342834", 
       "name": "zaandam, Zaandam, Borgerdiep", 
       "id": "37220780"
     }, 
     {
       "lat": "4.82732284203735", 
       "lon": "52.4667475670393", 
       "name": "zaandam, Zaandam, Borgerdiep", 
       "id": "37220790"
     }, 
     {
       "lat": "4.82234056631482", 
       "lon": "52.4650971865197", 
       "name": "zaandam, Zaandam, Sportvelden", 
       "id": "37220800"
     }, 
     {
       "lat": "4.8313489881231", 
       "lon": "52.4683932583589", 
       "name": "zaandam, Zaandam, De Twee Gebroeders", 
       "id": "37220810"
     }, 
     {
       "lat": "4.81786917651554", 
       "lon": "52.4603663058716", 
       "name": "zaandam, Zaandam, Jufferstraat", 
       "id": "37220820"
     }, 
     {
       "lat": "4.83507019480488", 
       "lon": "52.4685544440607", 
       "name": "zaandam, Zaandam, IJssel", 
       "id": "37220830"
     }, 
     {
       "lat": "4.8214810197451", 
       "lon": "52.4540653144673", 
       "name": "zaandam, Zaandam, Hof van Zaenden", 
       "id": "37220840"
     }, 
     {
       "lat": "4.8376898620839", 
       "lon": "52.4697260079371", 
       "name": "zaandam, Zaandam, Kennemerbeek", 
       "id": "37220850"
     }, 
     {
       "lat": "4.84259046889404", 
       "lon": "52.4709259853595", 
       "name": "zaandam, Zaandam, Schipbeek", 
       "id": "37220870"
     }, 
     {
       "lat": "4.84594602403857", 
       "lon": "52.4697190407843", 
       "name": "zaandam, Zaandam, Voorsterbeek", 
       "id": "37220890"
     }, 
     {
       "lat": "4.81254360749875", 
       "lon": "52.4501127186271", 
       "name": "zaandam, Zaandam, J. v. Goyenkade", 
       "id": "37220900"
     }, 
     {
       "lat": "4.84275500498806", 
       "lon": "52.4719063842482", 
       "name": "zaandam, Zaandam, Schipbeek", 
       "id": "37220920"
     }, 
     {
       "lat": "4.83025265978359", 
       "lon": "52.4596252270741", 
       "name": "zaandam, Zaandam, Fonteinkruidweg", 
       "id": "37220932"
     }, 
     {
       "lat": "4.8301789841525", 
       "lon": "52.4596338685533", 
       "name": "zaandam, Zaandam, Fonteinkruidweg", 
       "id": "37220933"
     }, 
     {
       "lat": "4.84256346774366", 
       "lon": "52.471923479852", 
       "name": "zaandam, Zaandam, Schipbeek", 
       "id": "37220940"
     }, 
     {
       "lat": "4.82771171772942", 
       "lon": "52.4592717357331", 
       "name": "zaandam, Zaandam, Leverkruidweg", 
       "id": "37220950"
     }, 
     {
       "lat": "4.82423369261145", 
       "lon": "52.4585632279399", 
       "name": "zaandam, Zaandam, Koekoeksbloemweg", 
       "id": "37220970"
     }, 
     {
       "lat": "4.81968065803906", 
       "lon": "52.4395866465462", 
       "name": "zaandam, Zaandam, Vinkenstraat", 
       "id": "37220980"
     }, 
     {
       "lat": "4.81951940437027", 
       "lon": "52.4578936427096", 
       "name": "zaandam, Zaandam, Zonnedauwhoek", 
       "id": "37220990"
     }, 
     {
       "lat": "4.82937289828525", 
       "lon": "52.4418795632623", 
       "name": "zaandam, Zaandam, Peperstraat", 
       "id": "37221001"
     }, 
     {
       "lat": "4.82937289828525", 
       "lon": "52.4418795632623", 
       "name": "zaandam, Zaandam, Peperstraat", 
       "id": "37221005"
     }, 
     {
       "lat": "4.82857390208757", 
       "lon": "52.4445900609474", 
       "name": "zaandam, Zaandam, Veldvliegerweg", 
       "id": "37221020"
     }, 
     {
       "lat": "4.8255968078282", 
       "lon": "52.4531771352165", 
       "name": "zaandam, Zaandam, Zaans Medisch Centrum", 
       "id": "37221030"
     }, 
     {
       "lat": "4.82760317791781", 
       "lon": "52.4492410649536", 
       "name": "zaandam, Zaandam, Kopermolenstraat", 
       "id": "37221040"
     }, 
     {
       "lat": "4.82726487008285", 
       "lon": "52.4492394674789", 
       "name": "zaandam, Zaandam, Kopermolenstraat", 
       "id": "37221050"
     }, 
     {
       "lat": "4.82555507230941", 
       "lon": "52.4529881978821", 
       "name": "zaandam, Zaandam, Zaans Medisch Centrum", 
       "id": "37221060"
     }, 
     {
       "lat": "4.82852217908909", 
       "lon": "52.4451919873639", 
       "name": "zaandam, Zaandam, Veldvliegerweg", 
       "id": "37221070"
     }, 
     {
       "lat": "4.81922401268919", 
       "lon": "52.4579821039415", 
       "name": "zaandam, Zaandam, Zonnedauwhoek", 
       "id": "37221101"
     }, 
     {
       "lat": "4.81975522393442", 
       "lon": "52.4395061148763", 
       "name": "zaandam, Zaandam, Vinkenstraat", 
       "id": "37221110"
     }, 
     {
       "lat": "4.824423349829", 
       "lon": "52.4586899546018", 
       "name": "zaandam, Zaandam, Koekoeksbloemweg", 
       "id": "37221121"
     }, 
     {
       "lat": "4.77049253206212", 
       "lon": "52.4655488786669", 
       "name": "westzaan, Westzaan, Kerkbuurt", 
       "id": "37221130"
     }, 
     {
       "lat": "4.82740230304429", 
       "lon": "52.4593062255975", 
       "name": "zaandam, Zaandam, Leverkruidweg", 
       "id": "37221141"
     }, 
     {
       "lat": "4.82379771548342", 
       "lon": "52.4731569826252", 
       "name": "zaandam, Zaandam, Zaanse Schans", 
       "id": "37221150"
     }, 
     {
       "lat": "4.82379771548342", 
       "lon": "52.4731569826252", 
       "name": "zaandam, Zaandam, Zaanse Schans", 
       "id": "37221160"
     }, 
     {
       "lat": "4.83790917033849", 
       "lon": "52.443770876894", 
       "name": "zaandam, Zaandam, Vermiljoenweg", 
       "id": "37221200"
     }, 
     {
       "lat": "4.84002649967037", 
       "lon": "52.445011971908", 
       "name": "zaandam, Zaandam, Meerpaal", 
       "id": "37221220"
     }, 
     {
       "lat": "4.85030432023151", 
       "lon": "52.4319550296053", 
       "name": "zaandam, Zaandam, Zuidervaart", 
       "id": "37221230"
     }, 
     {
       "lat": "4.83933288415589", 
       "lon": "52.4499519495238", 
       "name": "zaandam, Zaandam, Boeierlaan", 
       "id": "37221240"
     }, 
     {
       "lat": "4.85325235753646", 
       "lon": "52.4386731102704", 
       "name": "zaandam, Zaandam, Clusiusstraat", 
       "id": "37221290"
     }, 
     {
       "lat": "4.85286106976108", 
       "lon": "52.4406306456306", 
       "name": "zaandam, Zaandam, Dodonaeusstraat", 
       "id": "37221310"
     }, 
     {
       "lat": "4.84799699843313", 
       "lon": "52.446342710175", 
       "name": "zaandam, Zaandam, Brigantijnstraat", 
       "id": "37221320"
     }, 
     {
       "lat": "4.84472310033048", 
       "lon": "52.4494374821149", 
       "name": "zaandam, Zaandam, Barkstraat", 
       "id": "37221350"
     }, 
     {
       "lat": "4.84498588277663", 
       "lon": "52.4496004610372", 
       "name": "zaandam, Zaandam, Barkstraat", 
       "id": "37221360"
     }, 
     {
       "lat": "4.84824517589804", 
       "lon": "52.4464966279659", 
       "name": "zaandam, Zaandam, Brigantijnstraat", 
       "id": "37221370"
     }, 
     {
       "lat": "4.85264015080007", 
       "lon": "52.4406566123394", 
       "name": "zaandam, Zaandam, Dodonaeusstraat", 
       "id": "37221380"
     }, 
     {
       "lat": "4.85358075514628", 
       "lon": "52.438270146726", 
       "name": "zaandam, Zaandam, Clusiusstraat", 
       "id": "37221400"
     }, 
     {
       "lat": "4.83954248456198", 
       "lon": "52.4496563272749", 
       "name": "zaandam, Zaandam, Boeierlaan", 
       "id": "37221450"
     }, 
     {
       "lat": "4.85061428838054", 
       "lon": "52.4318575695509", 
       "name": "zaandam, Zaandam, Zuidervaart", 
       "id": "37221460"
     }, 
     {
       "lat": "4.84009226150732", 
       "lon": "52.4456414078772", 
       "name": "zaandam, Zaandam, Meerpaal", 
       "id": "37221470"
     }, 
     {
       "lat": "4.83792666576585", 
       "lon": "52.4435462676967", 
       "name": "zaandam, Zaandam, Vermiljoenweg", 
       "id": "37221490"
     }, 
     {
       "lat": "4.83286466520301", 
       "lon": "52.4413926379869", 
       "name": "zaandam, Zaandam, Het Mennistenerf", 
       "id": "37221510"
     }, 
     {
       "lat": "4.8254737629405", 
       "lon": "52.453598969487", 
       "name": "zaandam, Zaandam, Zaans Medisch Centrum", 
       "id": "37221530"
     }, 
     {
       "lat": "4.79730168091309", 
       "lon": "52.4701341415677", 
       "name": "zaandijk, Zaandijk, Simon Gammerkade", 
       "id": "37221580"
     }, 
     {
       "lat": "4.82476228208715", 
       "lon": "52.4216086172804", 
       "name": "zaandam, Zaandam, Zaanderhorn", 
       "id": "37221590"
     }, 
     {
       "lat": "4.82151942373462", 
       "lon": "52.4326479937832", 
       "name": "zaandam, Zaandam, Houthavenkade", 
       "id": "37221630"
     }, 
     {
       "lat": "4.79649828212677", 
       "lon": "52.4619694052088", 
       "name": "koog a/d zaan, Koog a/d Zaan, Westerkoogweg", 
       "id": "37221650"
     }, 
     {
       "lat": "4.80276208515206", 
       "lon": "52.4611915618646", 
       "name": "koog a/d zaan, Koog a/d Zaan, Oosterveld", 
       "id": "37221670"
     }, 
     {
       "lat": "4.80927873397117", 
       "lon": "52.4466725634152", 
       "name": "zaandam, Zaandam, Westerwateringtunnel", 
       "id": "37221790"
     }, 
     {
       "lat": "4.8093448821044", 
       "lon": "52.4472391061908", 
       "name": "zaandam, Zaandam, Westerwateringtunnel", 
       "id": "37221800"
     }, 
     {
       "lat": "4.80292291367345", 
       "lon": "52.4490141394737", 
       "name": "zaandam, Zaandam, De Westerwatering", 
       "id": "37221860"
     }, 
     {
       "lat": "4.79563693881914", 
       "lon": "52.4746645785235", 
       "name": "zaandijk, Zaandijk, Rotonde Rooswijk", 
       "id": "37221880"
     }, 
     {
       "lat": "4.79527393541224", 
       "lon": "52.4742942764268", 
       "name": "zaandijk, Zaandijk, Rotonde Rooswijk", 
       "id": "37221890"
     }, 
     {
       "lat": "4.80110957634863", 
       "lon": "52.477082445554", 
       "name": "zaandijk, Zaandijk, Verpleeghuis Rooswijk", 
       "id": "37221900"
     }, 
     {
       "lat": "4.79658211468675", 
       "lon": "52.4711191944245", 
       "name": "zaandijk, Zaandijk, Simon Gammerkade", 
       "id": "37221910"
     }, 
     {
       "lat": "4.79612188926642", 
       "lon": "52.4725189646072", 
       "name": "zaandijk, Zaandijk, Paukenhof", 
       "id": "37221920"
     }, 
     {
       "lat": "4.79628317269671", 
       "lon": "52.4725647063023", 
       "name": "zaandijk, Zaandijk, Paukenhof", 
       "id": "37221930"
     }, 
     {
       "lat": "4.80169421710475", 
       "lon": "52.47517098038", 
       "name": "zaandijk, Zaandijk, Bannehof", 
       "id": "37221940"
     }, 
     {
       "lat": "4.80187166114102", 
       "lon": "52.475108943286", 
       "name": "zaandijk, Zaandijk, Bannehof", 
       "id": "37221950"
     }, 
     {
       "lat": "4.80143516357168", 
       "lon": "52.4769492405555", 
       "name": "zaandijk, Zaandijk, Verpleeghuis Rooswijk", 
       "id": "37221960"
     }, 
     {
       "lat": "4.80317796702079", 
       "lon": "52.4720416323369", 
       "name": "zaandijk, Zaandijk, Oud Heinstraat", 
       "id": "37221970"
     }, 
     {
       "lat": "4.79806470682844", 
       "lon": "52.4758270737818", 
       "name": "zaandijk, Zaandijk, Gemeentehuis", 
       "id": "37221980"
     }, 
     {
       "lat": "4.79900449560991", 
       "lon": "52.4759935149611", 
       "name": "zaandijk, Zaandijk, Gemeentehuis", 
       "id": "37221990"
     }, 
     {
       "lat": "4.80234846959674", 
       "lon": "52.473556445085", 
       "name": "zaandijk, Zaandijk, Jan Steynstraat", 
       "id": "37222000"
     }, 
     {
       "lat": "4.80208130296222", 
       "lon": "52.4737258911611", 
       "name": "zaandijk, Zaandijk, Jan Steynstraat", 
       "id": "37222001"
     }, 
     {
       "lat": "4.82112503123664", 
       "lon": "52.442793148695", 
       "name": "zaandam, Zaandam, Botenmakersstraat", 
       "id": "37222010"
     }, 
     {
       "lat": "4.82168837079069", 
       "lon": "52.4424453203686", 
       "name": "zaandam, Zaandam, Botenmakersstraat", 
       "id": "37222020"
     }, 
     {
       "lat": "4.80106234675618", 
       "lon": "52.4517731423636", 
       "name": "zaandam, Zaandam, Hensbroekstraat", 
       "id": "37222090"
     }, 
     {
       "lat": "4.80086969007503", 
       "lon": "52.4518800411005", 
       "name": "zaandam, Zaandam, Hensbroekstraat", 
       "id": "37222110"
     }, 
     {
       "lat": "4.8445391211013", 
       "lon": "52.4380493429359", 
       "name": "zaandam, Zaandam, Smitsven", 
       "id": "37222200"
     }, 
     {
       "lat": "4.84465544220203", 
       "lon": "52.4381577268515", 
       "name": "zaandam, Zaandam, Smitsven", 
       "id": "37222201"
     }, 
     {
       "lat": "4.84727590818508", 
       "lon": "52.4343140044473", 
       "name": "zaandam, Zaandam, Schaarsven", 
       "id": "37222210"
     }, 
     {
       "lat": "4.84743710563118", 
       "lon": "52.4343596768026", 
       "name": "zaandam, Zaandam, Schaarsven", 
       "id": "37222211"
     }, 
     {
       "lat": "4.82875692215636", 
       "lon": "52.4417418484786", 
       "name": "zaandam, Zaandam, Peperstraat", 
       "id": "37223000"
     }, 
     {
       "lat": "4.8287130293012", 
       "lon": "52.4417236664343", 
       "name": "zaandam, Zaandam, Peperstraat", 
       "id": "37223001"
     }, 
     {
       "lat": "4.8421420038959", 
       "lon": "52.4416333897559", 
       "name": "zaandam, Zaandam, De Weer/Twiskeweg", 
       "id": "37223100"
     }, 
     {
       "lat": "4.85788626018208", 
       "lon": "52.4360964754755", 
       "name": "oostzaan, Oostzaan, Wateringbrug", 
       "id": "37223160"
     }, 
     {
       "lat": "4.8513252407048", 
       "lon": "52.4435806341868", 
       "name": "zaandam, Zaandam, Galjoenstraat", 
       "id": "37223200"
     }, 
     {
       "lat": "4.85124047982145", 
       "lon": "52.4432926476919", 
       "name": "zaandam, Zaandam, Galjoenstraat", 
       "id": "37223220"
     }, 
     {
       "lat": "4.84191985590499", 
       "lon": "52.4417581945877", 
       "name": "zaandam, Zaandam, De Weer", 
       "id": "37223230"
     }, 
     {
       "lat": "4.83225280014", 
       "lon": "52.442099796723", 
       "name": "zaandam, Zaandam, Het Mennistenerf", 
       "id": "37223500"
     }, 
     {
       "lat": "4.83310916225155", 
       "lon": "52.4418341744542", 
       "name": "zaandam, Zaandam, Het Mennistenerf", 
       "id": "37223501"
     }, 
     {
       "lat": "4.83581878655314", 
       "lon": "52.4391954625848", 
       "name": "zaandam, Zaandam, Walraven v.Hallstraat", 
       "id": "37223520"
     }, 
     {
       "lat": "4.8391613579015", 
       "lon": "52.4341059948674", 
       "name": "zaandam, Zaandam, Morgensterstraat", 
       "id": "37223540"
     }, 
     {
       "lat": "4.85659411742633", 
       "lon": "52.4297993644326", 
       "name": "zaandam, Zaandam, De Vlinder", 
       "id": "37223552"
     }, 
     {
       "lat": "4.84248469620817", 
       "lon": "52.4305172763756", 
       "name": "zaandam, Zaandam, Vijfhoek", 
       "id": "37223560"
     }, 
     {
       "lat": "4.84324931604438", 
       "lon": "52.4281210899189", 
       "name": "zaandam, Zaandam, Hotels Vijfhoek", 
       "id": "37223570"
     }, 
     {
       "lat": "4.84368317644681", 
       "lon": "52.4275119212407", 
       "name": "zaandam, Zaandam, Hotels Vijfhoek", 
       "id": "37223580"
     }, 
     {
       "lat": "4.84158195342302", 
       "lon": "52.4309894681772", 
       "name": "zaandam, Zaandam, Vijfhoek", 
       "id": "37223590"
     }, 
     {
       "lat": "4.85659411742633", 
       "lon": "52.4297993644326", 
       "name": "zaandam, Zaandam, De Vlinder", 
       "id": "37223600"
     }, 
     {
       "lat": "4.8564088005806", 
       "lon": "52.4293132027848", 
       "name": "zaandam, Zaandam, De Vlinder", 
       "id": "37223603"
     }, 
     {
       "lat": "4.85674792639023", 
       "lon": "52.4292338325719", 
       "name": "zaandam, Zaandam, De Vlinder", 
       "id": "37223607"
     }, 
     {
       "lat": "4.83880868382113", 
       "lon": "52.4340863882788", 
       "name": "zaandam, Zaandam, Morgensterstraat", 
       "id": "37223610"
     }, 
     {
       "lat": "4.8640313206851", 
       "lon": "52.4300301571271", 
       "name": "amsterdam, Amsterdam, Barndegat", 
       "id": "37223620"
     }, 
     {
       "lat": "4.83567799967712", 
       "lon": "52.4386915007764", 
       "name": "zaandam, Zaandam, Walraven v.Hallstraat", 
       "id": "37223630"
     }, 
     {
       "lat": "4.80336358133918", 
       "lon": "52.4479467832435", 
       "name": "zaandam, Zaandam, Winkelc. Lange Weide", 
       "id": "37223720"
     }, 
     {
       "lat": "4.82371983912925", 
       "lon": "52.4399923857827", 
       "name": "zaandam, Zaandam, Gedempte Gracht", 
       "id": "37223860"
     }, 
     {
       "lat": "4.81956992974948", 
       "lon": "52.4447809640796", 
       "name": "zaandam, Zaandam, Parkstraat", 
       "id": "37223880"
     }, 
     {
       "lat": "4.81966118403632", 
       "lon": "52.4502818217663", 
       "name": "zaandam, Zaandam, v.Goghweg", 
       "id": "37223900"
     }, 
     {
       "lat": "4.81228747136048", 
       "lon": "52.4539761498644", 
       "name": "zaandam, Zaandam, Frans Halsstraat", 
       "id": "37223920"
     }, 
     {
       "lat": "4.81122640833867", 
       "lon": "52.4552472398959", 
       "name": "zaandam, Zaandam, Breedweer", 
       "id": "37223940"
     }, 
     {
       "lat": "4.81123728369267", 
       "lon": "52.4634529702335", 
       "name": "koog a/d zaan, Koog a/d Zaan, Verzetstraat", 
       "id": "37223960"
     }, 
     {
       "lat": "4.81282663101157", 
       "lon": "52.4668400122921", 
       "name": "koog a/d zaan, Koog a/d Zaan, Boschjesstraat", 
       "id": "37223980"
     }, 
     {
       "lat": "4.81193845408106", 
       "lon": "52.4695050183173", 
       "name": "koog a/d zaan, Koog a/d Zaan, Stationsstraat", 
       "id": "37224000"
     }, 
     {
       "lat": "4.8110053540578", 
       "lon": "52.4710912892635", 
       "name": "zaandijk, Zaandijk, Guisweg/Zaanse Schans", 
       "id": "37224020"
     }, 
     {
       "lat": "4.81411876839826", 
       "lon": "52.4738745479742", 
       "name": "zaandijk, Zaandijk, Beeldentuin", 
       "id": "37224040"
     }, 
     {
       "lat": "4.81234452336512", 
       "lon": "52.4756275241286", 
       "name": "zaandijk, Zaandijk, Willem Dreeslaan", 
       "id": "37224060"
     }, 
     {
       "lat": "4.80902047903349", 
       "lon": "52.47769648052", 
       "name": "zaandijk, Zaandijk, Valkstraat", 
       "id": "37224080"
     }, 
     {
       "lat": "4.80846450060026", 
       "lon": "52.4796890077062", 
       "name": "zaandijk, Zaandijk, Koperslagerstraat", 
       "id": "37224290"
     }, 
     {
       "lat": "4.809092308849", 
       "lon": "52.4778316441394", 
       "name": "zaandijk, Zaandijk, Valkstraat", 
       "id": "37224310"
     }, 
     {
       "lat": "4.81247920272016", 
       "lon": "52.4754574131164", 
       "name": "zaandijk, Zaandijk, Willem Dreeslaan", 
       "id": "37224330"
     }, 
     {
       "lat": "4.81415942627816", 
       "lon": "52.4741443714839", 
       "name": "zaandijk, Zaandijk, Beeldentuin", 
       "id": "37224350"
     }, 
     {
       "lat": "4.81125377509205", 
       "lon": "52.4712273096862", 
       "name": "zaandijk, Zaandijk, Guisweg/Zaanse Schans", 
       "id": "37224370"
     }, 
     {
       "lat": "4.81224188190183", 
       "lon": "52.4688054587486", 
       "name": "koog a/d zaan, Koog a/d Zaan, Stationsstraat", 
       "id": "37224390"
     }, 
     {
       "lat": "4.8130167575383", 
       "lon": "52.4669308089113", 
       "name": "koog a/d zaan, Koog a/d Zaan, Boschjesstraat", 
       "id": "37224410"
     }, 
     {
       "lat": "4.81106130419783", 
       "lon": "52.4634071773246", 
       "name": "koog a/d zaan, Koog a/d Zaan, Verzetstraat", 
       "id": "37224430"
     }, 
     {
       "lat": "4.81124161579693", 
       "lon": "52.4585996897973", 
       "name": "koog a/d zaan, Koog a/d Zaan, Willem Alexanderbrug", 
       "id": "37224450"
     }, 
     {
       "lat": "4.81103528236985", 
       "lon": "52.4552373235966", 
       "name": "zaandam, Zaandam, Breedweer", 
       "id": "37224470"
     }, 
     {
       "lat": "4.81362062715576", 
       "lon": "52.4532725863403", 
       "name": "zaandam, Zaandam, Frans Halsstraat", 
       "id": "37224490"
     }, 
     {
       "lat": "4.81969394509446", 
       "lon": "52.450021337899", 
       "name": "zaandam, Zaandam, v.Goghweg", 
       "id": "37224510"
     }, 
     {
       "lat": "4.81952742088607", 
       "lon": "52.4446549338165", 
       "name": "zaandam, Zaandam, Parkstraat", 
       "id": "37224530"
     }, 
     {
       "lat": "4.82333782775422", 
       "lon": "52.439963606201", 
       "name": "zaandam, Zaandam, Gedempte Gracht", 
       "id": "37224550"
     }, 
     {
       "lat": "4.81256023936505", 
       "lon": "52.4375031577527", 
       "name": "zaandam, Zaandam, Houtveldweg/NS", 
       "id": "37224560"
     }, 
     {
       "lat": "4.81142003257426", 
       "lon": "52.4584567547867", 
       "name": "koog a/d zaan, Koog a/d Zaan, Willem Alexanderbrug", 
       "id": "37224600"
     }, 
     {
       "lat": "4.80598488179303", 
       "lon": "52.4566776519434", 
       "name": "koog a/d zaan, Koog a/d Zaan, Leliestraat", 
       "id": "37224610"
     }, 
     {
       "lat": "4.80642213164303", 
       "lon": "52.4558709099878", 
       "name": "koog a/d zaan, Koog a/d Zaan, Leliestraat", 
       "id": "37224620"
     }, 
     {
       "lat": "4.80351054837118", 
       "lon": "52.4479564946166", 
       "name": "zaandam, Zaandam, Winkelc. Lange Weide", 
       "id": "37224630"
     }, 
     {
       "lat": "4.80603879946912", 
       "lon": "52.4503326611369", 
       "name": "zaandam, Zaandam, Diepenbroekstraat", 
       "id": "37224660"
     }, 
     {
       "lat": "4.80628732482054", 
       "lon": "52.4504507183009", 
       "name": "zaandam, Zaandam, Diepenbroekstraat", 
       "id": "37224670"
     }, 
     {
       "lat": "4.80786427901522", 
       "lon": "52.4457309458666", 
       "name": "zaandam, Zaandam, Durgerdamstraat", 
       "id": "37224680"
     }, 
     {
       "lat": "4.80815808286668", 
       "lon": "52.4457593443109", 
       "name": "zaandam, Zaandam, Durgerdamstraat", 
       "id": "37224690"
     }, 
     {
       "lat": "4.80823711007164", 
       "lon": "52.4419669502624", 
       "name": "zaandam, Zaandam, Opera", 
       "id": "37224710"
     }, 
     {
       "lat": "4.80267724376014", 
       "lon": "52.4497948516236", 
       "name": "zaandam, Zaandam, De Westerwatering", 
       "id": "37224730"
     }, 
     {
       "lat": "4.80406170261948", 
       "lon": "52.4452000053295", 
       "name": "zaandam, Zaandam, Gaasperdamstraat", 
       "id": "37224750"
     }, 
     {
       "lat": "4.8043118509443", 
       "lon": "52.4451922480395", 
       "name": "zaandam, Zaandam, Gaasperdamstraat", 
       "id": "37224760"
     }, 
     {
       "lat": "4.79654686158447", 
       "lon": "52.4616371058686", 
       "name": "koog a/d zaan, Koog a/d Zaan, Westerkoogweg", 
       "id": "37224780"
     }, 
     {
       "lat": "4.80261235614836", 
       "lon": "52.46027408833", 
       "name": "koog a/d zaan, Koog a/d Zaan, Oosterveld", 
       "id": "37224800"
     }, 
     {
       "lat": "4.79839353411285", 
       "lon": "52.4566581684624", 
       "name": "koog a/d zaan, Koog a/d Zaan, Mallegatsloot", 
       "id": "37224810"
     }, 
     {
       "lat": "4.79829043439618", 
       "lon": "52.4566666439938", 
       "name": "koog a/d zaan, Koog a/d Zaan, Mallegatsloot", 
       "id": "37224820"
     }, 
     {
       "lat": "4.80834992848217", 
       "lon": "52.4412125399533", 
       "name": "zaandam, Zaandam, Opera", 
       "id": "37225080"
     }, 
     {
       "lat": "4.7991986392007", 
       "lon": "52.4525368483942", 
       "name": "zaandam, Zaandam, De Binding", 
       "id": "37225150"
     }, 
     {
       "lat": "4.79918787018561", 
       "lon": "52.4522402035051", 
       "name": "zaandam, Zaandam, De Binding", 
       "id": "37225160"
     }, 
     {
       "lat": "4.80633324827911", 
       "lon": "52.4637615882895", 
       "name": "koog a/d zaan, Koog a/d Zaan, Verzetstraat", 
       "id": "37225600"
     }, 
     {
       "lat": "4.80665907542679", 
       "lon": "52.4636014073462", 
       "name": "koog a/d zaan, Koog a/d Zaan, Verzetstraat", 
       "id": "37225610"
     }, 
     {
       "lat": "4.80568178589854", 
       "lon": "52.4696632404892", 
       "name": "zaandijk, Zaandijk, Station Koog/Zaandijk", 
       "id": "37225620"
     }, 
     {
       "lat": "4.80539172632447", 
       "lon": "52.469338264725", 
       "name": "koog a/d zaan, Koog a/d Zaan, Station Koog Zaandijk", 
       "id": "37225630"
     }, 
     {
       "lat": "4.8052543944336", 
       "lon": "52.4764198010717", 
       "name": "zaandijk, Zaandijk, Witte Veerstraat", 
       "id": "37225640"
     }, 
     {
       "lat": "4.80488608857849", 
       "lon": "52.4764449559413", 
       "name": "zaandijk, Zaandijk, Witte Veerstraat", 
       "id": "37225650"
     }, 
     {
       "lat": "4.85692574750885", 
       "lon": "52.4229792365929", 
       "name": "zaandam, Zaandam, Rijshoutweg", 
       "id": "37226010"
     }, 
     {
       "lat": "4.85296677404808", 
       "lon": "52.4209032840314", 
       "name": "zaandam, Zaandam, Bolbaken", 
       "id": "37226030"
     }, 
     {
       "lat": "4.85304626065671", 
       "lon": "52.4228449731191", 
       "name": "zaandam, Zaandam, Kruisbaken", 
       "id": "37226100"
     }, 
     {
       "lat": "4.85796118047128", 
       "lon": "52.43597997108", 
       "name": "oostzaan, Oostzaan, Wateringbrug", 
       "id": "37232670"
     }, 
     {
       "lat": "4.88525470578529", 
       "lon": "52.4281806231072", 
       "name": "oostzaan, Oostzaan, Zuideinde 239", 
       "id": "37233030"
     }, 
     {
       "lat": "4.88226186285842", 
       "lon": "52.4314753493357", 
       "name": "oostzaan, Oostzaan, Kolksloot", 
       "id": "37233050"
     }, 
     {
       "lat": "4.87929736386902", 
       "lon": "52.4348240460724", 
       "name": "oostzaan, Oostzaan, De Kolk", 
       "id": "37233070"
     }, 
     {
       "lat": "4.8771224703542", 
       "lon": "52.4372503457387", 
       "name": "oostzaan, Oostzaan, Lisweg", 
       "id": "37233090"
     }, 
     {
       "lat": "4.87551629938592", 
       "lon": "52.4400745155667", 
       "name": "oostzaan, Oostzaan, De Kunstgreep", 
       "id": "37233110"
     }, 
     {
       "lat": "4.86956024108757", 
       "lon": "52.438799378214", 
       "name": "oostzaan, Oostzaan, De Dors", 
       "id": "37233130"
     }, 
     {
       "lat": "4.86279882752533", 
       "lon": "52.4372597390356", 
       "name": "oostzaan, Oostzaan, Viaduct", 
       "id": "37233150"
     }, 
     {
       "lat": "4.86328441572622", 
       "lon": "52.4372349236498", 
       "name": "oostzaan, Oostzaan, Viaduct", 
       "id": "37233180"
     }, 
     {
       "lat": "4.86881088450415", 
       "lon": "52.4387421776436", 
       "name": "oostzaan, Oostzaan, De Dors", 
       "id": "37233200"
     }, 
     {
       "lat": "4.87566201014405", 
       "lon": "52.4401919832048", 
       "name": "oostzaan, Oostzaan, De Kunstgreep", 
       "id": "37233220"
     }, 
     {
       "lat": "4.87741802214661", 
       "lon": "52.4371257909034", 
       "name": "oostzaan, Oostzaan, Lisweg", 
       "id": "37233240"
     }, 
     {
       "lat": "4.87950219415349", 
       "lon": "52.4349147996677", 
       "name": "oostzaan, Oostzaan, De Kolk", 
       "id": "37233260"
     }, 
     {
       "lat": "4.88228870731786", 
       "lon": "52.431700153847", 
       "name": "oostzaan, Oostzaan, Kolksloot", 
       "id": "37233280"
     }, 
     {
       "lat": "4.88523664184505", 
       "lon": "52.4284771377309", 
       "name": "oostzaan, Oostzaan, Zuideinde 239", 
       "id": "37233300"
     }, 
     {
       "lat": "4.88894250148252", 
       "lon": "52.4244932892699", 
       "name": "amsterdam, Amsterdam, Zuideinde 319", 
       "id": "37233320"
     }, 
     {
       "lat": "4.74929412818175", 
       "lon": "52.4783609247968", 
       "name": "assendelft, Assendelft, Peters", 
       "id": "37320010"
     }, 
     {
       "lat": "4.79799741426633", 
       "lon": "52.4908179913063", 
       "name": "wormerveer, Wormerveer, Edisonstraat", 
       "id": "37320020"
     }, 
     {
       "lat": "4.75143163916378", 
       "lon": "52.4812124851343", 
       "name": "assendelft, Assendelft, Bruggeman", 
       "id": "37320030"
     }, 
     {
       "lat": "4.75756597040467", 
       "lon": "52.4877072858641", 
       "name": "assendelft, Assendelft, v.Gelderen", 
       "id": "37320050"
     }, 
     {
       "lat": "4.79326006353845", 
       "lon": "52.4894462334313", 
       "name": "wormerveer, Wormerveer, Station NS", 
       "id": "37320131"
     }, 
     {
       "lat": "4.79326006353845", 
       "lon": "52.4894462334313", 
       "name": "wormerveer, Wormerveer, Station NS", 
       "id": "37320132"
     }, 
     {
       "lat": "4.75115287355615", 
       "lon": "52.4811480772722", 
       "name": "assendelft, Assendelft, Bruggeman", 
       "id": "37320140"
     }, 
     {
       "lat": "4.77291251791923", 
       "lon": "52.509564586862", 
       "name": "krommenie, Krommenie, Willis/Zonnebaars", 
       "id": "37320200"
     }, 
     {
       "lat": "4.77291251791923", 
       "lon": "52.509564586862", 
       "name": "krommenie, Krommenie, Willis/Zonnebaars", 
       "id": "37320201"
     }, 
     {
       "lat": "4.76145893064707", 
       "lon": "52.4851933887809", 
       "name": "assendelft, Assendelft, Korenmeter", 
       "id": "37320230"
     }, 
     {
       "lat": "4.75714778062654", 
       "lon": "52.4839931922459", 
       "name": "assendelft, Assendelft, Waterrijklaan", 
       "id": "37320250"
     }, 
     {
       "lat": "4.75252377940293", 
       "lon": "52.4861435359724", 
       "name": "assendelft, Assendelft, Schenkerven", 
       "id": "37320290"
     }, 
     {
       "lat": "4.75258318010345", 
       "lon": "52.4861079034496", 
       "name": "assendelft, Assendelft, Schenkerven", 
       "id": "37320300"
     }, 
     {
       "lat": "4.74740947466269", 
       "lon": "52.4885696716869", 
       "name": "assendelft, Assendelft, H.P.Berlagestraat", 
       "id": "37320310"
     }, 
     {
       "lat": "4.75317831855349", 
       "lon": "52.4897780208303", 
       "name": "assendelft, Assendelft, Marathon", 
       "id": "37320330"
     }, 
     {
       "lat": "4.75347121963536", 
       "lon": "52.4898874370193", 
       "name": "assendelft, Assendelft, Marathon", 
       "id": "37320340"
     }, 
     {
       "lat": "4.74760164028041", 
       "lon": "52.4885167825125", 
       "name": "assendelft, Assendelft, H.P.Berlagestraat", 
       "id": "37320360"
     }, 
     {
       "lat": "4.75506518683816", 
       "lon": "52.4947672077704", 
       "name": "assendelft, Assendelft, Station NS Saendelverlaan", 
       "id": "37320410"
     }, 
     {
       "lat": "4.7550658295826", 
       "lon": "52.4947222733453", 
       "name": "assendelft, Assendelft, Station NS Saendelverlaan", 
       "id": "37320411"
     }, 
     {
       "lat": "4.75437383067786", 
       "lon": "52.4854613767077", 
       "name": "assendelft, Assendelft, Noorderveenweg", 
       "id": "37320420"
     }, 
     {
       "lat": "4.75453666127082", 
       "lon": "52.4853993322352", 
       "name": "assendelft, Assendelft, Noorderveenweg", 
       "id": "37320430"
     }, 
     {
       "lat": "4.78433421559773", 
       "lon": "52.5048148421551", 
       "name": "wormerveer, Wormerveer, Samsonweg", 
       "id": "37320440"
     }, 
     {
       "lat": "4.78423100080926", 
       "lon": "52.5048233051927", 
       "name": "wormerveer, Wormerveer, Samsonweg", 
       "id": "37320450"
     }, 
     {
       "lat": "4.75445004950919", 
       "lon": "52.4955638219674", 
       "name": "assendelft, Assendelft, Station NS Prov.weg", 
       "id": "37320460"
     }, 
     {
       "lat": "4.7533454578103", 
       "lon": "52.4996832177047", 
       "name": "krommenie, Krommenie, Neptunuslaan", 
       "id": "37323830"
     }, 
     {
       "lat": "4.75270026658265", 
       "lon": "52.5015401937642", 
       "name": "krommenie, Krommenie, Grote Beer", 
       "id": "37323850"
     }, 
     {
       "lat": "4.7545753094204", 
       "lon": "52.5043003984166", 
       "name": "krommenie, Krommenie, Armstrongbrug", 
       "id": "37323870"
     }, 
     {
       "lat": "4.7567059445218", 
       "lon": "52.5077449826272", 
       "name": "krommenie, Krommenie, Glennstraat", 
       "id": "37323890"
     }, 
     {
       "lat": "4.7581767336806", 
       "lon": "52.5078965896439", 
       "name": "krommenie, Krommenie, Glennstraat", 
       "id": "37323891"
     }, 
     {
       "lat": "4.76003233124711", 
       "lon": "52.5068818326769", 
       "name": "krommenie, Krommenie, Kervelstraat", 
       "id": "37323910"
     }, 
     {
       "lat": "4.76858469229709", 
       "lon": "52.5051561857482", 
       "name": "krommenie, Krommenie, Blok", 
       "id": "37323930"
     }, 
     {
       "lat": "4.76645552666031", 
       "lon": "52.5015500477212", 
       "name": "krommenie, Krommenie, Heiligeweg", 
       "id": "37323970"
     }, 
     {
       "lat": "4.76655869737328", 
       "lon": "52.4994475007949", 
       "name": "krommenie, Krommenie, Badhuislaan", 
       "id": "37323990"
     }, 
     {
       "lat": "4.77269008125482", 
       "lon": "52.4980234352731", 
       "name": "krommenie, Krommenie, Padlaan", 
       "id": "37324010"
     }, 
     {
       "lat": "4.77881587449684", 
       "lon": "52.4969765021228", 
       "name": "wormerveer, Wormerveer, De Noordse Balk", 
       "id": "37324030"
     }, 
     {
       "lat": "4.7824772248998", 
       "lon": "52.4962941934643", 
       "name": "wormerveer, Wormerveer, Krokusstraat", 
       "id": "37324050"
     }, 
     {
       "lat": "4.78539093803351", 
       "lon": "52.4986008334691", 
       "name": "wormerveer, Wormerveer, Westerstraat", 
       "id": "37324070"
     }, 
     {
       "lat": "4.78687424668668", 
       "lon": "52.4999834418097", 
       "name": "wormerveer, Wormerveer, Cor Bruijnweg", 
       "id": "37324090"
     }, 
     {
       "lat": "4.80858390018118", 
       "lon": "52.4795637644207", 
       "name": "zaandijk, Zaandijk, Koperslagerstraat", 
       "id": "37324100"
     }, 
     {
       "lat": "4.78926566035658", 
       "lon": "52.4984766249144", 
       "name": "wormerveer, Wormerveer, Lijsterstraat", 
       "id": "37324110"
     }, 
     {
       "lat": "4.80754176409154", 
       "lon": "52.4827043211623", 
       "name": "wormerveer, Wormerveer, Schildersbuurt", 
       "id": "37324120"
     }, 
     {
       "lat": "4.78796404299497", 
       "lon": "52.4956389821171", 
       "name": "wormerveer, Wormerveer, Noorderstraat", 
       "id": "37324130"
     }, 
     {
       "lat": "4.80616022774374", 
       "lon": "52.4847736863776", 
       "name": "wormerveer, Wormerveer, Plein 13", 
       "id": "37324140"
     }, 
     {
       "lat": "4.79216344099249", 
       "lon": "52.494347938836", 
       "name": "wormerveer, Wormerveer, Noordeinde", 
       "id": "37324150"
     }, 
     {
       "lat": "4.80180553333135", 
       "lon": "52.4867744737229", 
       "name": "wormerveer, Wormerveer, Warmoesstraat", 
       "id": "37324160"
     }, 
     {
       "lat": "4.79090422957084", 
       "lon": "52.4916363643554", 
       "name": "wormerveer, Wormerveer, Zaanweg", 
       "id": "37324170"
     }, 
     {
       "lat": "4.79374710758879", 
       "lon": "52.4893587955862", 
       "name": "wormerveer, Wormerveer, Station NS", 
       "id": "37324190"
     }, 
     {
       "lat": "4.79363439655939", 
       "lon": "52.4900772357639", 
       "name": "wormerveer, Wormerveer, Station NS", 
       "id": "37324200"
     }, 
     {
       "lat": "4.79100316930381", 
       "lon": "52.4919424383403", 
       "name": "wormerveer, Wormerveer, Zaanweg", 
       "id": "37324220"
     }, 
     {
       "lat": "4.80222177821205", 
       "lon": "52.4864709505085", 
       "name": "wormerveer, Wormerveer, Warmoesstraat", 
       "id": "37324230"
     }, 
     {
       "lat": "4.79241314384236", 
       "lon": "52.4943941287856", 
       "name": "wormerveer, Wormerveer, Noordeinde", 
       "id": "37324240"
     }, 
     {
       "lat": "4.8061260609659", 
       "lon": "52.4851330210861", 
       "name": "wormerveer, Wormerveer, Plein 13", 
       "id": "37324250"
     }, 
     {
       "lat": "4.78793166938816", 
       "lon": "52.4958545196342", 
       "name": "wormerveer, Wormerveer, Noorderstraat", 
       "id": "37324260"
     }, 
     {
       "lat": "4.80719036745925", 
       "lon": "52.4825588024049", 
       "name": "wormerveer, Wormerveer, Schildersbuurt", 
       "id": "37324270"
     }, 
     {
       "lat": "4.78936983204173", 
       "lon": "52.498396262063", 
       "name": "wormerveer, Wormerveer, Lijsterstraat", 
       "id": "37324280"
     }, 
     {
       "lat": "4.78678418200371", 
       "lon": "52.5001088115439", 
       "name": "wormerveer, Wormerveer, Cor Bruijnweg", 
       "id": "37324300"
     }, 
     {
       "lat": "4.78514183105257", 
       "lon": "52.4985096941588", 
       "name": "wormerveer, Wormerveer, Westerstraat", 
       "id": "37324320"
     }, 
     {
       "lat": "4.78253452473976", 
       "lon": "52.4964113236377", 
       "name": "wormerveer, Wormerveer, Krokusstraat", 
       "id": "37324340"
     }, 
     {
       "lat": "4.7788730417849", 
       "lon": "52.497102620947", 
       "name": "wormerveer, Wormerveer, De Noordse Balk", 
       "id": "37324360"
     }, 
     {
       "lat": "4.77217207404013", 
       "lon": "52.4982094895035", 
       "name": "krommenie, Krommenie, Padlaan", 
       "id": "37324380"
     }, 
     {
       "lat": "4.76750365784237", 
       "lon": "52.4992726894927", 
       "name": "krommenie, Krommenie, Badhuislaan", 
       "id": "37324400"
     }, 
     {
       "lat": "4.76629959901629", 
       "lon": "52.5011178294604", 
       "name": "krommenie, Krommenie, Heiligeweg", 
       "id": "37324420"
     }, 
     {
       "lat": "4.7687619258295", 
       "lon": "52.5051211595316", 
       "name": "krommenie, Krommenie, Blok", 
       "id": "37324460"
     }, 
     {
       "lat": "4.7543409613998", 
       "lon": "52.5042092731127", 
       "name": "krommenie, Krommenie, Armstrongbrug", 
       "id": "37324520"
     }, 
     {
       "lat": "4.75303652039104", 
       "lon": "52.5017127552056", 
       "name": "krommenie, Krommenie, Grote Beer", 
       "id": "37324540"
     }, 
     {
       "lat": "4.75260426991674", 
       "lon": "52.5000207827031", 
       "name": "krommenie, Krommenie, Neptunuslaan", 
       "id": "37324560"
     }, 
     {
       "lat": "4.7611872346394", 
       "lon": "52.506456529671", 
       "name": "krommenie, Krommenie, Kervelstraat", 
       "id": "37324580"
     }, 
     {
       "lat": "4.76176416908844", 
       "lon": "52.5062798214087", 
       "name": "krommenie, Krommenie, Rosariumhorst", 
       "id": "37324600"
     }, 
     {
       "lat": "4.75525514968655", 
       "lon": "52.4979588060439", 
       "name": "krommenie, Krommenie, Jupiterstraat", 
       "id": "37324620"
     }, 
     {
       "lat": "4.75545988776159", 
       "lon": "52.4980587596746", 
       "name": "krommenie, Krommenie, Jupiterstraat", 
       "id": "37324621"
     }, 
     {
       "lat": "4.75392325272865", 
       "lon": "52.5189645805408", 
       "name": "krommeniedijk, Krommeniedijk, Woudpolderweg", 
       "id": "37325030"
     }, 
     {
       "lat": "4.75384804557369", 
       "lon": "52.519072029459", 
       "name": "krommeniedijk, Krommeniedijk, Woudpolderweg", 
       "id": "37325040"
     }, 
     {
       "lat": "4.76019837703201", 
       "lon": "52.5169757085239", 
       "name": "krommeniedijk, Krommeniedijk, Brandweer", 
       "id": "37325050"
     }, 
     {
       "lat": "4.75985942604097", 
       "lon": "52.516982904692", 
       "name": "krommeniedijk, Krommeniedijk, Brandweer", 
       "id": "37325060"
     }, 
     {
       "lat": "4.76718279101888", 
       "lon": "52.5147924884125", 
       "name": "krommeniedijk, Krommeniedijk, School", 
       "id": "37325070"
     }, 
     {
       "lat": "4.76737391225256", 
       "lon": "52.5148204494051", 
       "name": "krommeniedijk, Krommeniedijk, School", 
       "id": "37325080"
     }, 
     {
       "lat": "4.77097361929576", 
       "lon": "52.5081165285148", 
       "name": "krommeniedijk, Krommeniedijk, Vlusch", 
       "id": "37325090"
     }, 
     {
       "lat": "4.77116571666928", 
       "lon": "52.508072588356", 
       "name": "krommeniedijk, Krommeniedijk, Vlusch", 
       "id": "37325100"
     }, 
     {
       "lat": "4.76248394303815", 
       "lon": "52.5053758715731", 
       "name": "krommenie, Krommenie, Rosariumhorst", 
       "id": "37325130"
     }, 
     {
       "lat": "4.76248394303815", 
       "lon": "52.5053758715731", 
       "name": "krommenie, Krommenie, Rosariumhorst", 
       "id": "37325131"
     }, 
     {
       "lat": "4.76840481484639", 
       "lon": "52.5043283940661", 
       "name": "krommenie, Krommenie, Eikenlaan", 
       "id": "37325160"
     }, 
     {
       "lat": "4.78752819600429", 
       "lon": "52.4941178845166", 
       "name": "wormerveer, Wormerveer, Marktplein", 
       "id": "37325170"
     }, 
     {
       "lat": "4.78752490350353", 
       "lon": "52.4943605316413", 
       "name": "wormerveer, Wormerveer, Marktplein", 
       "id": "37325180"
     }, 
     {
       "lat": "4.77790146932183", 
       "lon": "52.496010141472", 
       "name": "wormerveer, Wormerveer, Noordse Balk", 
       "id": "37325190"
     }, 
     {
       "lat": "4.77790146932183", 
       "lon": "52.496010141472", 
       "name": "wormerveer, Wormerveer, Noordse Balk", 
       "id": "37325191"
     }, 
     {
       "lat": "4.74913092715039", 
       "lon": "52.4784499229227", 
       "name": "assendelft, Assendelft, Peters", 
       "id": "37330020"
     }, 
     {
       "lat": "4.74620181555616", 
       "lon": "52.4743807141352", 
       "name": "assendelft, Assendelft, R.K. Kerk", 
       "id": "37330040"
     }, 
     {
       "lat": "4.74499428314043", 
       "lon": "52.4723969046249", 
       "name": "assendelft, Assendelft, Rijkhof", 
       "id": "37330060"
     }, 
     {
       "lat": "4.74307965455876", 
       "lon": "52.469456554195", 
       "name": "assendelft, Assendelft, Hornlaan", 
       "id": "37330080"
     }, 
     {
       "lat": "4.74511515782931", 
       "lon": "52.4671128346499", 
       "name": "assendelft, Assendelft, Festina Lente", 
       "id": "37330100"
     }, 
     {
       "lat": "4.73770801151821", 
       "lon": "52.4624438574175", 
       "name": "assendelft, Assendelft, Genieweg", 
       "id": "37330140"
     }, 
     {
       "lat": "4.73486569648917", 
       "lon": "52.4576198586077", 
       "name": "assendelft, Assendelft, Zaandammerweg", 
       "id": "37330150"
     }, 
     {
       "lat": "4.73654611488223", 
       "lon": "52.4604062781084", 
       "name": "assendelft, Assendelft, De Zaaier", 
       "id": "37330160"
     }, 
     {
       "lat": "4.73703947331199", 
       "lon": "52.4608763424344", 
       "name": "assendelft, Assendelft, De Zaaier", 
       "id": "37330170"
     }, 
     {
       "lat": "4.73427206977957", 
       "lon": "52.4569694793041", 
       "name": "assendelft, Assendelft, Zaandammerweg", 
       "id": "37330180"
     }, 
     {
       "lat": "4.738116817068", 
       "lon": "52.4626617996355", 
       "name": "assendelft, Assendelft, Genieweg", 
       "id": "37330190"
     }, 
     {
       "lat": "4.73954606527309", 
       "lon": "52.4645390451537", 
       "name": "assendelft, Assendelft, Simone de Beauvoirstraat", 
       "id": "37330210"
     }, 
     {
       "lat": "4.74454689568023", 
       "lon": "52.4667232879144", 
       "name": "assendelft, Assendelft, Festina Lente", 
       "id": "37330230"
     }, 
     {
       "lat": "4.7430925377177", 
       "lon": "52.4695824509785", 
       "name": "assendelft, Assendelft, Hornlaan", 
       "id": "37330250"
     }, 
     {
       "lat": "4.74436865628105", 
       "lon": "52.4718991955779", 
       "name": "assendelft, Assendelft, Rijkhof", 
       "id": "37330270"
     }, 
     {
       "lat": "4.74645135722658", 
       "lon": "52.4744270007909", 
       "name": "assendelft, Assendelft, R.K. Kerk", 
       "id": "37330290"
     }, 
     {
       "lat": "4.73963316472201", 
       "lon": "52.4646204096507", 
       "name": "assendelft, Assendelft, Simone de Beauvoirstraat", 
       "id": "37330340"
     }, 
     {
       "lat": "4.76411157869279", 
       "lon": "52.4651560141456", 
       "name": "assendelft, Assendelft, Watertoren", 
       "id": "37330590"
     }, 
     {
       "lat": "4.76381716817929", 
       "lon": "52.4651634542868", 
       "name": "assendelft, Assendelft, Watertoren", 
       "id": "37330600"
     }, 
     {
       "lat": "4.75340891151069", 
       "lon": "52.4716422784828", 
       "name": "assendelft, Assendelft, Veenpolderdijk", 
       "id": "37330610"
     }, 
     {
       "lat": "4.75339149034194", 
       "lon": "52.471830925318", 
       "name": "assendelft, Assendelft, Veenpolderdijk", 
       "id": "37330620"
     }, 
     {
       "lat": "4.73998260358461", 
       "lon": "52.4658805871276", 
       "name": "assendelft, Assendelft, Gemeentehuis", 
       "id": "37330690"
     }, 
     {
       "lat": "4.740506539703", 
       "lon": "52.4662789018997", 
       "name": "assendelft, Assendelft, Gemeentehuis", 
       "id": "37330700"
     }, 
     {
       "lat": "4.85198278780682", 
       "lon": "52.4767746999993", 
       "name": "ONBEKEND, Wormerland, P&R A7 / afrit 2", 
       "id": "37340010"
     }, 
     {
       "lat": "4.79698250039973", 
       "lon": "52.4907410454729", 
       "name": "wormerveer, Wormerveer, Edisonstraat", 
       "id": "37420010"
     }, 
     {
       "lat": "4.79927927461943", 
       "lon": "52.4918579190221", 
       "name": "wormer, Wormer, Nieuweweg", 
       "id": "37420030"
     }, 
     {
       "lat": "4.80297725495559", 
       "lon": "52.4961452688895", 
       "name": "wormer, Wormer, Rotonde Ned Benedictweg", 
       "id": "37420050"
     }, 
     {
       "lat": "4.81197595415428", 
       "lon": "52.4983013107254", 
       "name": "wormer, Wormer, Zaandammerstraat", 
       "id": "37420140"
     }, 
     {
       "lat": "4.80655978567156", 
       "lon": "52.4969447723903", 
       "name": "wormer, Wormer, Badhuisstraat", 
       "id": "37420160"
     }, 
     {
       "lat": "4.80303413380159", 
       "lon": "52.4962983370268", 
       "name": "wormer, Wormer, Rotonde Ned Benedictweg", 
       "id": "37420180"
     }, 
     {
       "lat": "4.79917286460159", 
       "lon": "52.4921090427989", 
       "name": "wormer, Wormer, Nieuweweg", 
       "id": "37420200"
     }, 
     {
       "lat": "4.80356788583794", 
       "lon": "52.4937934421111", 
       "name": "wormer, Wormer, Rouenweg", 
       "id": "37420210"
     }, 
     {
       "lat": "4.80303106355104", 
       "lon": "52.4931886348159", 
       "name": "wormer, Wormer, Rouenweg", 
       "id": "37420230"
     }, 
     {
       "lat": "4.8022639574735", 
       "lon": "52.4955216142258", 
       "name": "wormer, Wormer, Zandweg", 
       "id": "37420240"
     }, 
     {
       "lat": "4.80201292885132", 
       "lon": "52.4955743014218", 
       "name": "wormer, Wormer, Zandweg", 
       "id": "37420250"
     }, 
     {
       "lat": "4.812886679901", 
       "lon": "52.4950792017547", 
       "name": "wormer, Wormer, Spatterstraat", 
       "id": "37420260"
     }, 
     {
       "lat": "4.81361791115475", 
       "lon": "52.4920629294494", 
       "name": "wormer, Wormer, Waterzolder", 
       "id": "37420280"
     }, 
     {
       "lat": "4.80817454081836", 
       "lon": "52.490589491009", 
       "name": "wormer, Wormer, De Balk", 
       "id": "37420300"
     }, 
     {
       "lat": "4.79495579217476", 
       "lon": "52.5068366025207", 
       "name": "oost knollendam, Oost Knollendam, Weromerie", 
       "id": "37424010"
     }, 
     {
       "lat": "4.79479474666407", 
       "lon": "52.5067638984349", 
       "name": "oost knollendam, Oost Knollendam, Weromerie", 
       "id": "37424020"
     }, 
     {
       "lat": "4.79058462317855", 
       "lon": "52.5142204138888", 
       "name": "oost knollendam, Oost Knollendam, Voetbalveld", 
       "id": "37424030"
     }, 
     {
       "lat": "4.79037778762349", 
       "lon": "52.5142643113362", 
       "name": "oost knollendam, Oost Knollendam, Voetbalveld", 
       "id": "37424040"
     }, 
     {
       "lat": "4.79057110954414", 
       "lon": "52.5174019215531", 
       "name": "oost knollendam, Oost Knollendam, Pleintje", 
       "id": "37424050"
     }, 
     {
       "lat": "4.79023434647638", 
       "lon": "52.5172474405143", 
       "name": "oost knollendam, Oost Knollendam, Pleintje", 
       "id": "37424060"
     }, 
     {
       "lat": "4.79461815835835", 
       "lon": "52.5210261833649", 
       "name": "oost knollendam, Oost Knollendam, Toldeurkering", 
       "id": "37424070"
     }, 
     {
       "lat": "4.80880782558806", 
       "lon": "52.4950773603409", 
       "name": "wormer, Wormer, Spatterstraat/Sporthal", 
       "id": "37424090"
     }, 
     {
       "lat": "4.80880782558806", 
       "lon": "52.4950773603409", 
       "name": "wormer, Wormer, Spatterstraat/Sporthal", 
       "id": "37424091"
     }, 
     {
       "lat": "4.81634057701621", 
       "lon": "52.4978640291331", 
       "name": "wormer, Wormer, Torenerf", 
       "id": "37424110"
     }, 
     {
       "lat": "4.81634057701621", 
       "lon": "52.4978640291331", 
       "name": "wormer, Wormer, Torenerf", 
       "id": "37424111"
     }, 
     {
       "lat": "4.81133702608621", 
       "lon": "52.4987385996759", 
       "name": "wormer, Wormer, Talingstraat", 
       "id": "37424130"
     }, 
     {
       "lat": "4.81133702608621", 
       "lon": "52.4987385996759", 
       "name": "wormer, Wormer, Talingstraat", 
       "id": "37424131"
     }, 
     {
       "lat": "5.07214845138995", 
       "lon": "52.6585488443472", 
       "name": "hoorn, Hoorn, Oostergouw", 
       "id": "38113210"
     }, 
     {
       "lat": "5.07167480161622", 
       "lon": "52.658646446659", 
       "name": "hoorn, Hoorn, Oostergouw", 
       "id": "38113220"
     }, 
     {
       "lat": "4.63492085359247", 
       "lon": "52.3078738727404", 
       "name": "hoofddorp, Hoofddorp, Oosterschelde", 
       "id": "56230260"
     }, 
     {
       "lat": "4.63448328464723", 
       "lon": "52.3077362683635", 
       "name": "hoofddorp, Hoofddorp, Oosterschelde", 
       "id": "56230270"
     }, 
     {
       "lat": "4.63000798959548", 
       "lon": "52.276069770987", 
       "name": "nieuw-vennep, Nieuw-Vennep, Getsewoud Noord", 
       "id": "56430130"
     }, 
     {
       "lat": "4.62956998298807", 
       "lon": "52.2759770837019", 
       "name": "nieuw-vennep, Nieuw-Vennep, Getsewoud Noord", 
       "id": "56430140"
     }, 
     {
       "lat": "4.90432038804378", 
       "lon": "52.3745945877576", 
       "name": "amsterdam, Amsterdam, Pr.Hendrikkade", 
       "id": "57003042"
     }, 
     {
       "lat": "4.8993061780877", 
       "lon": "52.4219120284421", 
       "name": "amsterdam, Amsterdam, P.A. van Heijningestraat", 
       "id": "57111530"
     }, 
     {
       "lat": "4.89930548510145", 
       "lon": "52.4219749388858", 
       "name": "amsterdam, Amsterdam, P.A. van Heijningestraat", 
       "id": "57111540"
     }, 
     {
       "lat": "4.90983056263874", 
       "lon": "52.4234018973591", 
       "name": "landsmeer, Landsmeer, Zuideinde 90", 
       "id": "57112400"
     }, 
     {
       "lat": "4.91208140465157", 
       "lon": "52.3985871173174", 
       "name": "amsterdam, Amsterdam, Pinksterbloemstraat", 
       "id": "57112550"
     }, 
     {
       "lat": "4.91347671606352", 
       "lon": "52.393137199353", 
       "name": "amsterdam, Amsterdam, Mosplein", 
       "id": "57112590"
     }, 
     {
       "lat": "4.91390255079669", 
       "lon": "52.3931568770294", 
       "name": "amsterdam, Amsterdam, Mosplein", 
       "id": "57112620"
     }, 
     {
       "lat": "4.91213738066113", 
       "lon": "52.3988479836673", 
       "name": "amsterdam, Amsterdam, Pinksterbloemstraat", 
       "id": "57112660"
     }, 
     {
       "lat": "4.89190587893662", 
       "lon": "52.421117380556", 
       "name": "amsterdam, Amsterdam, Molenaarsweg", 
       "id": "57112990"
     }, 
     {
       "lat": "4.88890072438635", 
       "lon": "52.4242863984529", 
       "name": "amsterdam, Amsterdam, Zuideinde 319", 
       "id": "57113010"
     }, 
     {
       "lat": "4.89586561830183", 
       "lon": "52.4034102509839", 
       "name": "amsterdam, Amsterdam, Klaprozenweg", 
       "id": "57113330"
     }, 
     {
       "lat": "4.89194756664806", 
       "lon": "52.4213332576643", 
       "name": "amsterdam, Amsterdam, Molenaarsweg", 
       "id": "57113340"
     }, 
     {
       "lat": "4.895877422697", 
       "lon": "52.403670941803", 
       "name": "amsterdam, Amsterdam, Klaprozenweg", 
       "id": "57113820"
     }, 
     {
       "lat": "4.88048970078488", 
       "lon": "52.4128723903999", 
       "name": "amsterdam, Amsterdam, Keerkringpark", 
       "id": "57114530"
     }, 
     {
       "lat": "4.880464212869", 
       "lon": "52.412530750978", 
       "name": "amsterdam, Amsterdam, Keerkringpark", 
       "id": "57114540"
     }, 
     {
       "lat": "4.89148385634101", 
       "lon": "52.4075982162036", 
       "name": "amsterdam, Amsterdam, Stenendokweg", 
       "id": "57114550"
     }, 
     {
       "lat": "4.89166442157958", 
       "lon": "52.4072214904837", 
       "name": "amsterdam, Amsterdam, Stenendokweg", 
       "id": "57114560"
     }, 
     {
       "lat": "4.84324812954765", 
       "lon": "52.3923052175377", 
       "name": "amsterdam, Amsterdam, Einsteinweg/Basisweg", 
       "id": "57120010"
     }, 
     {
       "lat": "4.84506839176494", 
       "lon": "52.3924214158907", 
       "name": "amsterdam, Amsterdam, Einsteinweg/Basisweg", 
       "id": "57120020"
     }, 
     {
       "lat": "4.84030460971185", 
       "lon": "52.3915456826101", 
       "name": "amsterdam, Amsterdam, La Guardiaweg", 
       "id": "57120040"
     }, 
     {
       "lat": "4.86420807183029", 
       "lon": "52.4300039744027", 
       "name": "amsterdam, Amsterdam, Barndegat", 
       "id": "57123530"
     }, 
     {
       "lat": "4.81444916341975", 
       "lon": "52.3357981273356", 
       "name": "amsterdam, Amsterdam, Anderlechtlaan", 
       "id": "57132300"
     }, 
     {
       "lat": "4.81483027243214", 
       "lon": "52.33582693488", 
       "name": "amsterdam, Amsterdam, Anderlechtlaan", 
       "id": "57132310"
     }, 
     {
       "lat": "4.82780102408301", 
       "lon": "52.3451104551253", 
       "name": "amsterdam, Amsterdam, Henk Sneevlietweg", 
       "id": "57134040"
     }, 
     {
       "lat": "4.82723494331655", 
       "lon": "52.3550842261975", 
       "name": "amsterdam, Amsterdam, Pieter Calandlaan", 
       "id": "57134050"
     }, 
     {
       "lat": "4.82733555410969", 
       "lon": "52.3505997968389", 
       "name": "amsterdam, Amsterdam, Johan Huizingalaan", 
       "id": "57134070"
     }, 
     {
       "lat": "4.82753444964217", 
       "lon": "52.351122029291", 
       "name": "amsterdam, Amsterdam, Johan Huizingalaan", 
       "id": "57134080"
     }, 
     {
       "lat": "4.82745783106236", 
       "lon": "52.3548695736427", 
       "name": "amsterdam, Amsterdam, Pieter Calandlaan", 
       "id": "57134100"
     }, 
     {
       "lat": "4.82750419090811", 
       "lon": "52.3442102716388", 
       "name": "amsterdam, Amsterdam, Henk Sneevlietweg", 
       "id": "57134110"
     }, 
     {
       "lat": "4.81130217174696", 
       "lon": "52.3340841534118", 
       "name": "amsterdam, Amsterdam, Oude Haagseweg", 
       "id": "57232610"
     }, 
     {
       "lat": "4.81055559329899", 
       "lon": "52.333954687793", 
       "name": "amsterdam, Amsterdam, Oude Haagseweg", 
       "id": "57232620"
     }, 
     {
       "lat": "4.79956724026242", 
       "lon": "52.3228096218992", 
       "name": "ONBEKEND, Schiphol Noord, Cateringweg", 
       "id": "57330230"
     }, 
     {
       "lat": "4.79956735915814", 
       "lon": "52.3228006346313", 
       "name": "ONBEKEND, Schiphol Noord, Cateringweg", 
       "id": "57330240"
     }, 
     {
       "lat": "4.79544872570026", 
       "lon": "52.3236699032764", 
       "name": "badhoevedorp, Badhoevedorp, Ibis Hotel", 
       "id": "57330290"
     }, 
     {
       "lat": "4.79543310045833", 
       "lon": "52.3237417279975", 
       "name": "badhoevedorp, Badhoevedorp, Ibis Hotel", 
       "id": "57330320"
     }, 
     {
       "lat": "4.96431800799693", 
       "lon": "52.2673034661758", 
       "name": "abcoude, Abcoude, Viadukt A2", 
       "id": "57452000"
     }, 
     {
       "lat": "4.70978482615246", 
       "lon": "52.2602136443887", 
       "name": "rijsenhout, Rijsenhout, Bennebroekerweg", 
       "id": "57542170"
     }, 
     {
       "lat": "4.70571165167136", 
       "lon": "52.2555074576254", 
       "name": "rijsenhout, Rijsenhout, Kleine Poellaan", 
       "id": "57542410"
     }, 
     {
       "lat": "4.71258096605376", 
       "lon": "52.2554839564289", 
       "name": "rijsenhout, Rijsenhout, Leimuiderdijk 42", 
       "id": "57542420"
     }, 
     {
       "lat": "4.71312292200586", 
       "lon": "52.2583811966575", 
       "name": "rijsenhout, Rijsenhout, Schrevelsgerecht", 
       "id": "57542430"
     }, 
     {
       "lat": "4.70964271226924", 
       "lon": "52.2531931711604", 
       "name": "rijsenhout, Rijsenhout, Blauwe Beugel", 
       "id": "57542440"
     }, 
     {
       "lat": "4.85764305058617", 
       "lon": "52.5596464322926", 
       "name": "De Rijp, De Rijp, Oosteinde", 
       "id": "36380040"
     }, 
     {
       "lat": "4.85755587003199", 
       "lon": "52.5595381951097", 
       "name": "De Rijp, De Rijp, Oosteinde", 
       "id": "36380050"
     }, 
     {
       "lat": "4.85028670822982", 
       "lon": "52.5594606163035", 
       "name": "De Rijp, De Rijp, Grote Dam", 
       "id": "36380070"
     }, 
     {
       "lat": "4.8434965415341", 
       "lon": "52.5600049152096", 
       "name": "De Rijp, De Rijp, Wollandje", 
       "id": "36380561"
     }, 
     {
       "lat": "4.84314729304187", 
       "lon": "52.5596258459677", 
       "name": "De Rijp, De Rijp, Wollandje", 
       "id": "36380562"
     }, 
     {
       "lat": "4.84532588261921", 
       "lon": "52.5527424846784", 
       "name": "t.h.v. Op/afrit N244, t.h.v. Op/afrit N244", 
       "id": "36389619"
     }, 
     {
       "lat": "4.849042416783", 
       "lon": "52.5514562151776", 
       "name": "t.h.v. Op/afrit N244, t.h.v. Op/afrit N244", 
       "id": "36389629"
     }, 
     {
       "lat": "4.91093141644844", 
       "lon": "52.5451867623689", 
       "name": "Middenbeemster, Middenbeemster, K.Hogetoornlaan", 
       "id": "36470070"
     }, 
     {
       "lat": "4.90380072731197", 
       "lon": "52.5501728944172", 
       "name": "Middenbeemster, Middenbeemster, Insulindeweg", 
       "id": "36470090"
     }, 
     {
       "lat": "4.90783616281068", 
       "lon": "52.5492096319114", 
       "name": "Middenbeemster, Middenbeemster, N. Cromhoutlaan", 
       "id": "36470110"
     }, 
     {
       "lat": "4.90297138132636", 
       "lon": "52.5505110349247", 
       "name": "Middenbeemster, Middenbeemster, Insulindeweg", 
       "id": "36470120"
     }, 
     {
       "lat": "4.91274440087292", 
       "lon": "52.5479531403872", 
       "name": "Middenbeemster, Middenbeemster, de Buurt", 
       "id": "36470130"
     }, 
     {
       "lat": "4.91218613590956", 
       "lon": "52.5477711612365", 
       "name": "Middenbeemster, Middenbeemster, de Buurt", 
       "id": "36470140"
     }, 
     {
       "lat": "4.90811636812013", 
       "lon": "52.5492017754115", 
       "name": "Middenbeemster, Middenbeemster, N. Cromhoutlaan", 
       "id": "36470160"
     }, 
     {
       "lat": "4.88725913657689", 
       "lon": "52.5540228928354", 
       "name": "Westbeemster, Westbeemster, Blikken Schel", 
       "id": "36470180"
     }, 
     {
       "lat": "4.88802908279374", 
       "lon": "52.5537385363168", 
       "name": "Westbeemster, Westbeemster, Blikken Schel", 
       "id": "36470190"
     }, 
     {
       "lat": "4.93861480174843", 
       "lon": "52.5424545738655", 
       "name": "Beemster, Beemster, Nekkerweg", 
       "id": "36470220"
     }, 
     {
       "lat": "4.93863072946438", 
       "lon": "52.5423377984308", 
       "name": "Beemster, Beemster, Nekkerweg", 
       "id": "36470230"
     }, 
     {
       "lat": "4.91984953825719", 
       "lon": "52.5466422020523", 
       "name": "Middenbeemster, Middenbeemster, Groenveld", 
       "id": "36470240"
     }, 
     {
       "lat": "4.91983593873321", 
       "lon": "52.5465343002478", 
       "name": "Middenbeemster, Middenbeemster, Groenveld", 
       "id": "36470250"
     }, 
     {
       "lat": "4.91294827904448", 
       "lon": "52.5481876261424", 
       "name": "Middenbeemster, Middenbeemster, de Buurt", 
       "id": "36470260"
     }, 
     {
       "lat": "4.91290511505778", 
       "lon": "52.5480885928093", 
       "name": "Middenbeemster, Middenbeemster, de Buurt", 
       "id": "36470270"
     }, 
     {
       "lat": "4.85984806118449", 
       "lon": "52.5602314355437", 
       "name": "Westbeemster, Westbeemster, Klaterbuurt", 
       "id": "36470280"
     }, 
     {
       "lat": "4.85977551267568", 
       "lon": "52.560132252363", 
       "name": "Westbeemster, Westbeemster, Klaterbuurt", 
       "id": "36470290"
     }, 
     {
       "lat": "4.91191591033319", 
       "lon": "52.5468533692484", 
       "name": "Middenbeemster, Middenbeemster, Middelwijck", 
       "id": "36470310"
     }, 
     {
       "lat": "4.91204887621837", 
       "lon": "52.5468269393263", 
       "name": "Middenbeemster, Middenbeemster, Middelwijck", 
       "id": "36470320"
     }, 
     {
       "lat": "4.91063649594788", 
       "lon": "52.545194566387", 
       "name": "Middenbeemster, Middenbeemster, K.Hogetoornlaan", 
       "id": "36470330"
     }, 
     {
       "lat": "4.91057840479688", 
       "lon": "52.545113446933", 
       "name": "Middenbeemster, Middenbeemster, K.Hogetoornlaan", 
       "id": "36470340"
     }, 
     {
       "lat": "4.90641088312947", 
       "lon": "52.547415384761", 
       "name": "Middenbeemster, Middenbeemster, Westerhem", 
       "id": "36470350"
     }, 
     {
       "lat": "4.90629216432749", 
       "lon": "52.5474868028933", 
       "name": "Middenbeemster, Middenbeemster, Westerhem", 
       "id": "36470360"
     }, 
     {
       "lat": "4.90743987381829", 
       "lon": "52.5490462589836", 
       "name": "Middenbeemster, Middenbeemster, N. Cromhoutlaan", 
       "id": "36470370"
     }, 
     {
       "lat": "4.90730689849456", 
       "lon": "52.5490726837179", 
       "name": "Middenbeemster, Middenbeemster, N. Cromhoutlaan", 
       "id": "36470380"
     }, 
     {
       "lat": "4.88683043698513", 
       "lon": "52.5541199481867", 
       "name": "Westbeemster, Westbeemster, Blikken Schel", 
       "id": "36470390"
     }, 
     {
       "lat": "4.88677258183224", 
       "lon": "52.5540208434297", 
       "name": "Westbeemster, Westbeemster, Blikken Schel", 
       "id": "36470400"
     }, 
     {
       "lat": "4.9296317392192", 
       "lon": "52.5444424503155", 
       "name": "t.h.v. Rijperweg, t.h.v. Rijperweg", 
       "id": "36479920"
     }, 
     {
       "lat": "4.92957389366755", 
       "lon": "52.5443343791176", 
       "name": "t.h.v. Rijperweg, t.h.v. Rijperweg", 
       "id": "36479930"
     }, 
     {
       "lat": "4.93823707946112", 
       "lon": "52.5158235337177", 
       "name": "Zuidoostbeemster, Zuidoostbeemster, Zuiderhof", 
       "id": "36570100"
     }, 
     {
       "lat": "4.94698207263534", 
       "lon": "52.5223182318448", 
       "name": "Zuidoostbeemster, Zuidoostbeemster, Volgerweg", 
       "id": "36570160"
     }, 
     {
       "lat": "4.94677553340483", 
       "lon": "52.5223444278225", 
       "name": "Zuidoostbeemster, Zuidoostbeemster, Volgerweg", 
       "id": "36570170"
     }, 
     {
       "lat": "4.95644725536673", 
       "lon": "52.53833250243", 
       "name": "Beemster, Beemster, Rijperweg/Purmerenderweg", 
       "id": "36570180"
     }, 
     {
       "lat": "4.9457537863728", 
       "lon": "52.5125353770714", 
       "name": "t.h.v. Beemsterbrug, t.h.v. Beemsterbrug", 
       "id": "36579910"
     }, 
     {
       "lat": "4.94612078836755", 
       "lon": "52.5126625654165", 
       "name": "t.h.v. Beemsterbrug, t.h.v. Beemsterbrug", 
       "id": "36579920"
     }, 
     {
       "lat": "4.95098081173409", 
       "lon": "52.4381743029396", 
       "name": "Watergang, Watergang, Dorp", 
       "id": "37200030"
     }, 
     {
       "lat": "4.95126895281893", 
       "lon": "52.4268330558797", 
       "name": "Watergang, Watergang, Pontje", 
       "id": "37200040"
     }, 
     {
       "lat": "4.95098846010933", 
       "lon": "52.4254569244818", 
       "name": "Watergang, Watergang, Pontje", 
       "id": "37200070"
     }, 
     {
       "lat": "4.95114993176942", 
       "lon": "52.4389208921443", 
       "name": "Watergang, Watergang, Dorp", 
       "id": "37200080"
     }, 
     {
       "lat": "4.94897588092691", 
       "lon": "52.4490687997826", 
       "name": "Ilpendam, Ilpendam, Jaagweg", 
       "id": "37200510"
     }, 
     {
       "lat": "4.95196829491399", 
       "lon": "52.4214970034048", 
       "name": "Schouw, Schouw, Splitsing", 
       "id": "37200530"
     }, 
     {
       "lat": "4.9528846162643", 
       "lon": "52.4224979871034", 
       "name": "Schouw, Schouw, Splitsing", 
       "id": "37200540"
     }, 
     {
       "lat": "4.99727098690115", 
       "lon": "52.433689056573", 
       "name": "Broek in Waterland, Broek in Waterland, Dorp", 
       "id": "37201010"
     }, 
     {
       "lat": "4.95487390468617", 
       "lon": "52.4220199315642", 
       "name": "Schouw, Schouw, Splitsing", 
       "id": "37201020"
     }, 
     {
       "lat": "4.9753769890795", 
       "lon": "52.4240792091133", 
       "name": "Broek in Waterland, Broek in Waterland, Kruisweg", 
       "id": "37201030"
     }, 
     {
       "lat": "4.9767696642265", 
       "lon": "52.4245064561224", 
       "name": "Broek in Waterland, Broek in Waterland, Kruisweg", 
       "id": "37201040"
     }, 
     {
       "lat": "4.95509212848164", 
       "lon": "52.4222544046324", 
       "name": "Schouw, Schouw, Splitsing", 
       "id": "37201050"
     }, 
     {
       "lat": "5.01360632323021", 
       "lon": "52.4408328257736", 
       "name": "t.h.v. Broek in Waterland, t.h.v. Broek in Waterland", 
       "id": "37209639"
     }, 
     {
       "lat": "4.94803643882101", 
       "lon": "52.4192176248618", 
       "name": "t.h.v. Schouw, t.h.v. Schouw", 
       "id": "37209649"
     }, 
     {
       "lat": "4.94760864348218", 
       "lon": "52.4193688277166", 
       "name": "t.h.v. Schouw, t.h.v. Schouw", 
       "id": "37209659"
     }, 
     {
       "lat": "4.91874881784424", 
       "lon": "52.4350314770614", 
       "name": "Landsmeer, Landsmeer, Zwanebloemweg", 
       "id": "37212040"
     }, 
     {
       "lat": "4.91461367956899", 
       "lon": "52.4394459365148", 
       "name": "Landsmeer, Landsmeer, Noordeinde Nr 78", 
       "id": "37212100"
     }, 
     {
       "lat": "4.91408966561569", 
       "lon": "52.4416907386365", 
       "name": "Landsmeer, Landsmeer, Noordeinde Nr 40", 
       "id": "37212120"
     }, 
     {
       "lat": "4.91378149968728", 
       "lon": "52.4443767903386", 
       "name": "Landsmeer, Landsmeer, Vermaning", 
       "id": "37212140"
     }, 
     {
       "lat": "4.91129093379834", 
       "lon": "52.4475663895287", 
       "name": "Den Ilp, Den Ilp, Nr 38", 
       "id": "37212160"
     }, 
     {
       "lat": "4.91586492179933", 
       "lon": "52.4351908079062", 
       "name": "Landsmeer, Landsmeer, Vogelwikkestraat", 
       "id": "37212251"
     }, 
     {
       "lat": "4.91557063967657", 
       "lon": "52.4352076124439", 
       "name": "Landsmeer, Landsmeer, Vogelwikkestraat", 
       "id": "37212252"
     }, 
     {
       "lat": "4.91817467652201", 
       "lon": "52.4350921195302", 
       "name": "Landsmeer, Landsmeer, Zwanebloemweg", 
       "id": "37212271"
     }, 
     {
       "lat": "4.91837377957124", 
       "lon": "52.4329538632001", 
       "name": "Landsmeer, Landsmeer, Fuutstraat", 
       "id": "37212290"
     }, 
     {
       "lat": "4.91346081532742", 
       "lon": "52.4289887761499", 
       "name": "Landsmeer, Landsmeer, van Beekstraat", 
       "id": "37212350"
     }, 
     {
       "lat": "4.91346081532742", 
       "lon": "52.4289887761499", 
       "name": "Landsmeer, Landsmeer, van Beekstraat", 
       "id": "37212360"
     }, 
     {
       "lat": "4.91095237392304", 
       "lon": "52.4257162248401", 
       "name": "Landsmeer, Landsmeer, Luyendijk", 
       "id": "37212370"
     }, 
     {
       "lat": "4.90586589526576", 
       "lon": "52.4256776993087", 
       "name": "Landsmeer, Landsmeer, Burg. Postweg", 
       "id": "37212380"
     }, 
     {
       "lat": "4.9063590085637", 
       "lon": "52.4262998456854", 
       "name": "Landsmeer, Landsmeer, Burg. Postweg", 
       "id": "37212390"
     }, 
     {
       "lat": "4.90598931158882", 
       "lon": "52.4237908035327", 
       "name": "Landsmeer, Landsmeer, Scheepsbouwersweg", 
       "id": "37212400"
     }, 
     {
       "lat": "4.90546673252419", 
       "lon": "52.4231775230222", 
       "name": "Landsmeer, Landsmeer, Scheepsbouwersweg", 
       "id": "37212410"
     }, 
     {
       "lat": "4.90988457609948", 
       "lon": "52.4265747384296", 
       "name": "Landsmeer, Landsmeer, Geijenbreek", 
       "id": "37212420"
     }, 
     {
       "lat": "4.90975187358806", 
       "lon": "52.4266101542686", 
       "name": "Landsmeer, Landsmeer, Geijenbreek", 
       "id": "37212430"
     }, 
     {
       "lat": "4.91548692606045", 
       "lon": "52.4375440493709", 
       "name": "Landsmeer, Landsmeer, Dotterbloemstraat", 
       "id": "37212480"
     }, 
     {
       "lat": "4.91481598112349", 
       "lon": "52.4384041844737", 
       "name": "Landsmeer, Landsmeer, Noordeinde t/o 106", 
       "id": "37212520"
     }, 
     {
       "lat": "4.91462586362305", 
       "lon": "52.4383045633346", 
       "name": "Landsmeer, Landsmeer, Noordeinde t/o 106", 
       "id": "37212540"
     }, 
     {
       "lat": "4.91090667161588", 
       "lon": "52.4477356099089", 
       "name": "Den Ilp, Den Ilp, Nr 38", 
       "id": "37212630"
     }, 
     {
       "lat": "4.91369661910682", 
       "lon": "52.444061886614", 
       "name": "Landsmeer, Landsmeer, Vermaning", 
       "id": "37212670"
     }, 
     {
       "lat": "4.91407803269519", 
       "lon": "52.4414030900276", 
       "name": "Landsmeer, Landsmeer, Noordeinde Nr 40", 
       "id": "37212690"
     }, 
     {
       "lat": "4.91481793252073", 
       "lon": "52.4395995393979", 
       "name": "Landsmeer, Landsmeer, Noordeinde Nr 78", 
       "id": "37212710"
     }, 
     {
       "lat": "4.91463862252712", 
       "lon": "52.4371092667129", 
       "name": "Landsmeer, Landsmeer, Noordeinde Nr 122", 
       "id": "37212731"
     }, 
     {
       "lat": "4.91464015737947", 
       "lon": "52.4369654716099", 
       "name": "Landsmeer, Landsmeer, Noordeinde Nr 122", 
       "id": "37212732"
     }, 
     {
       "lat": "4.91466934665363", 
       "lon": "52.4356084637323", 
       "name": "Landsmeer, Landsmeer, Varenstraat", 
       "id": "37212750"
     }, 
     {
       "lat": "4.91466723644318", 
       "lon": "52.4358061820554", 
       "name": "Landsmeer, Landsmeer, Varenstraat", 
       "id": "37212751"
     }, 
     {
       "lat": "4.91340498629158", 
       "lon": "52.428709937597", 
       "name": "Landsmeer, Landsmeer, van Beekstraat", 
       "id": "37212830"
     }, 
     {
       "lat": "4.91334569594973", 
       "lon": "52.4287546385145", 
       "name": "Landsmeer, Landsmeer, van Beekstraat", 
       "id": "37214100"
     }, 
     {
       "lat": "4.91373641561731", 
       "lon": "52.4444664859082", 
       "name": "t.h.v. Vermaning, t.h.v. Vermaning", 
       "id": "37219619"
     }, 
     {
       "lat": "4.91372737992711", 
       "lon": "52.44393618359", 
       "name": "t.h.v. Vermaning, t.h.v. Vermaning", 
       "id": "37219629"
     }, 
     {
       "lat": "4.94911491212799", 
       "lon": "52.4647435473804", 
       "name": "Ilpendam, Ilpendam, Dorp", 
       "id": "37300520"
     }, 
     {
       "lat": "4.94745640902117", 
       "lon": "52.4776344605417", 
       "name": "Ilpendam, Ilpendam, Purmerlandersteiger", 
       "id": "37301010"
     }, 
     {
       "lat": "4.94900066871949", 
       "lon": "52.4643926126021", 
       "name": "Ilpendam, Ilpendam, Dorp", 
       "id": "37301030"
     }, 
     {
       "lat": "4.94768860327838", 
       "lon": "52.4779678579086", 
       "name": "t.h.v. Purmelandersteiger, t.h.v. Purmelandersteiger", 
       "id": "37309619"
     }, 
     {
       "lat": "4.94745640902117", 
       "lon": "52.4776344605417", 
       "name": "t.h.v. Purmerlandersteiger, t.h.v. Purmerlandersteiger", 
       "id": "37309629"
     }, 
     {
       "lat": "4.9231198503153", 
       "lon": "52.4781708598912", 
       "name": "Purmerland, Purmerland, Ilperrijweg Nr 81", 
       "id": "37311240"
     }, 
     {
       "lat": "4.91024025809783", 
       "lon": "52.4645306469897", 
       "name": "Den Ilp, Den Ilp, Nr 180", 
       "id": "37312300"
     }, 
     {
       "lat": "4.91232346482996", 
       "lon": "52.4664893002635", 
       "name": "Den Ilp, Den Ilp, Nr 186", 
       "id": "37312320"
     }, 
     {
       "lat": "4.91794336729881", 
       "lon": "52.4721738047557", 
       "name": "Purmerland, Purmerland, Oostzanerrijweg", 
       "id": "37312340"
     }, 
     {
       "lat": "4.93116377661346", 
       "lon": "52.4903261651313", 
       "name": "Purmerland, Purmerland, Melkweg Nr 21", 
       "id": "37312350"
     }, 
     {
       "lat": "4.92099923042735", 
       "lon": "52.4754752822911", 
       "name": "Purmerland, Purmerland, Ilperrijweg Nr 93", 
       "id": "37312360"
     }, 
     {
       "lat": "4.92749365269841", 
       "lon": "52.4850453420303", 
       "name": "Purmerland, Purmerland, Melkweg Nr 26", 
       "id": "37312370"
     }, 
     {
       "lat": "4.92307871230265", 
       "lon": "52.4778830991686", 
       "name": "Purmerland, Purmerland, Ilperrijweg Nr 81", 
       "id": "37312380"
     }, 
     {
       "lat": "4.92537283065085", 
       "lon": "52.4809028626334", 
       "name": "Purmerland, Purmerland, Purmerlanderkerk", 
       "id": "37312390"
     }, 
     {
       "lat": "4.92582614216779", 
       "lon": "52.4811922262681", 
       "name": "Purmerland, Purmerland, Purmerlanderkerk", 
       "id": "37312400"
     }, 
     {
       "lat": "4.92798941058789", 
       "lon": "52.4855056234928", 
       "name": "Purmerland, Purmerland, Melkweg Nr 26", 
       "id": "37312420"
     }, 
     {
       "lat": "4.92056063208042", 
       "lon": "52.4751949449821", 
       "name": "Purmerland, Purmerland, Ilperrijweg Nr 93", 
       "id": "37312430"
     }, 
     {
       "lat": "4.93131174714467", 
       "lon": "52.4902548341461", 
       "name": "Purmerland, Purmerland, Melkweg Nr 21", 
       "id": "37312440"
     }, 
     {
       "lat": "4.91703818460243", 
       "lon": "52.4714871691187", 
       "name": "Purmerland, Purmerland, Oostzanerrijweg", 
       "id": "37312450"
     }, 
     {
       "lat": "4.91230672370198", 
       "lon": "52.4666779711582", 
       "name": "Den Ilp, Den Ilp, Nr 186", 
       "id": "37312470"
     }, 
     {
       "lat": "4.91010695725276", 
       "lon": "52.4646109984824", 
       "name": "Den Ilp, Den Ilp, Nr 180", 
       "id": "37312490"
     }, 
     {
       "lat": "4.79686471812296", 
       "lon": "52.4907404593769", 
       "name": "t.h.v. Zaanbrug, t.h.v. Zaanbrug", 
       "id": "37329601"
     }, 
     {
       "lat": "4.79796772902374", 
       "lon": "52.4908358189474", 
       "name": "t.h.v. Zaanbrug, t.h.v. Zaanbrug", 
       "id": "37329602"
     }, 
     {
       "lat": "5.03204280879666", 
       "lon": "52.456249123174", 
       "name": "Monnickendam, Monnickendam, Grote Kerk", 
       "id": "37390020"
     }, 
     {
       "lat": "5.03204280879666", 
       "lon": "52.456249123174", 
       "name": "Monnickendam, Monnickendam, Grote Kerk", 
       "id": "37390021"
     }, 
     {
       "lat": "5.03110755126046", 
       "lon": "52.4554644073433", 
       "name": "Monnickendam, Monnickendam, Nieuwpoortslaan", 
       "id": "37390070"
     }, 
     {
       "lat": "5.03110755126046", 
       "lon": "52.4554644073433", 
       "name": "Monnickendam, Monnickendam, Nieuwpoortslaan", 
       "id": "37390072"
     }, 
     {
       "lat": "5.02993083234388", 
       "lon": "52.4499695120794", 
       "name": "Monnickendam, Monnickendam, Ringshemmen", 
       "id": "37390090"
     }, 
     {
       "lat": "5.02993083234388", 
       "lon": "52.4499695120794", 
       "name": "Monnickendam, Monnickendam, Ringshemmen", 
       "id": "37390091"
     }, 
     {
       "lat": "5.03859834185068", 
       "lon": "52.4495459376031", 
       "name": "Monnickendam, Monnickendam, Ooster Ee", 
       "id": "37390110"
     }, 
     {
       "lat": "5.03859834185068", 
       "lon": "52.4495459376031", 
       "name": "Monnickendam, Monnickendam, Ooster Ee", 
       "id": "37390112"
     }, 
     {
       "lat": "5.0383872163214", 
       "lon": "52.4520708010936", 
       "name": "Monnickendam, Monnickendam, Pierebaan", 
       "id": "37390130"
     }, 
     {
       "lat": "5.0383872163214", 
       "lon": "52.4520708010936", 
       "name": "Monnickendam, Monnickendam, Pierebaan", 
       "id": "37390132"
     }, 
     {
       "lat": "5.03778768651472", 
       "lon": "52.4553404799573", 
       "name": "Monnickendam, Monnickendam, Swaensborch", 
       "id": "37390150"
     }, 
     {
       "lat": "5.03768378387335", 
       "lon": "52.4554570109915", 
       "name": "Monnickendam, Monnickendam, Swaensborch", 
       "id": "37390151"
     }, 
     {
       "lat": "5.03763922357783", 
       "lon": "52.4555108045219", 
       "name": "Monnickendam, Monnickendam, Swaensborch", 
       "id": "37390152"
     }, 
     {
       "lat": "5.03254729160266", 
       "lon": "52.4667300240061", 
       "name": "Katwoude, Katwoude, Lagedijk", 
       "id": "37390510"
     }, 
     {
       "lat": "4.99831387748363", 
       "lon": "52.4338183082818", 
       "name": "Broek in Waterland, Broek in Waterland, Dorp", 
       "id": "37390520"
     }, 
     {
       "lat": "5.04547482035362", 
       "lon": "52.45626162968", 
       "name": "Monnickendam, Monnickendam, Cornelis Dirkszlaan", 
       "id": "37391020"
     }, 
     {
       "lat": "5.06294557692257", 
       "lon": "52.4371583539917", 
       "name": "Zuiderwoude, Zuiderwoude, Dijkeinde", 
       "id": "37391030"
     }, 
     {
       "lat": "5.04469579432455", 
       "lon": "52.4561695073945", 
       "name": "Monnickendam, Monnickendam, Cornelis Dirkszlaan", 
       "id": "37391040"
     }, 
     {
       "lat": "5.04446701954623", 
       "lon": "52.4553150360854", 
       "name": "Monnickendam, Monnickendam, Cornelis Dirkszlaan", 
       "id": "37391050"
     }, 
     {
       "lat": "5.06407913888893", 
       "lon": "52.4369906864888", 
       "name": "Zuiderwoude, Zuiderwoude, Dijkeinde", 
       "id": "37391060"
     }, 
     {
       "lat": "5.03901580101022", 
       "lon": "52.452575947775", 
       "name": "Monnickendam, Monnickendam, Jan Nieuwenhuyzenlaan", 
       "id": "37391070"
     }, 
     {
       "lat": "5.04769897434389", 
       "lon": "52.4405758612176", 
       "name": "Zuiderwoude, Zuiderwoude, Gouw", 
       "id": "37391090"
     }, 
     {
       "lat": "5.04798376909862", 
       "lon": "52.4398756510285", 
       "name": "Zuiderwoude, Zuiderwoude, Gouw", 
       "id": "37391100"
     }, 
     {
       "lat": "5.04777559119325", 
       "lon": "52.447846966324", 
       "name": "Monnickendam, Monnickendam, Bereklauw", 
       "id": "37391110"
     }, 
     {
       "lat": "5.0483680762629", 
       "lon": "52.4473094115048", 
       "name": "Monnickendam, Monnickendam, Bereklauw", 
       "id": "37391120"
     }, 
     {
       "lat": "5.02883237209423", 
       "lon": "52.4548284291779", 
       "name": "Monnickendam, Monnickendam, Bernhardbrug", 
       "id": "37392510"
     }, 
     {
       "lat": "5.03098641323998", 
       "lon": "52.4577199012213", 
       "name": "Monnickendam, Monnickendam, Bernhardbrug", 
       "id": "37392520"
     }, 
     {
       "lat": "5.01410528588812", 
       "lon": "52.4409602224225", 
       "name": "t.h.v. Broek in Waterland, t.h.v. Broek in Waterland", 
       "id": "37399639"
     }, 
     {
       "lat": "5.04811715810777", 
       "lon": "52.4397412200337", 
       "name": "t.h.v. Gouw, t.h.v. Gouw", 
       "id": "37399649"
     }, 
     {
       "lat": "5.04793751539267", 
       "lon": "52.440154131351", 
       "name": "t.h.v. Gouw, t.h.v. Gouw", 
       "id": "37399659"
     }, 
     {
       "lat": "4.96239105420053", 
       "lon": "52.5241538817701", 
       "name": "Purmerend, Purmerend, M.L. Kingweg", 
       "id": "37400010"
     }, 
     {
       "lat": "4.94588990358345", 
       "lon": "52.5018588259006", 
       "name": "Purmerend, Purmerend, Rozenstraat", 
       "id": "37400020"
     }, 
     {
       "lat": "4.95633833883933", 
       "lon": "52.516268099058", 
       "name": "Purmerend, Purmerend, Wilgenhoek", 
       "id": "37400021"
     }, 
     {
       "lat": "4.95602300982458", 
       "lon": "52.5168780969547", 
       "name": "Purmerend, Purmerend, Wilgenhoek", 
       "id": "37400022"
     }, 
     {
       "lat": "4.95746168895799", 
       "lon": "52.5249719644046", 
       "name": "Purmerend, Purmerend, Aalscholverstraat", 
       "id": "37400023"
     }, 
     {
       "lat": "4.95731688111772", 
       "lon": "52.5247108060275", 
       "name": "Purmerend, Purmerend, Aalscholverstraat", 
       "id": "37400024"
     }, 
     {
       "lat": "4.96618548689016", 
       "lon": "52.4893501652676", 
       "name": "Purmerend, Purmerend, Brahmsstraat", 
       "id": "37400030"
     }, 
     {
       "lat": "4.96618548689016", 
       "lon": "52.4893501652676", 
       "name": "Purmerend, Purmerend, Brahmsstraat", 
       "id": "37400031"
     }, 
     {
       "lat": "4.96619267653476", 
       "lon": "52.4885952451649", 
       "name": "Purmerend, Purmerend, Brahmsstraat", 
       "id": "37400032"
     }, 
     {
       "lat": "4.94992221180583", 
       "lon": "52.4902529918023", 
       "name": "Purmerend, Purmerend, Vurige Staart", 
       "id": "37400040"
     }, 
     {
       "lat": "4.95711657895993", 
       "lon": "52.5210701896883", 
       "name": "Purmerend, Purmerend, Sternstraat", 
       "id": "37400050"
     }, 
     {
       "lat": "4.94770377419465", 
       "lon": "52.4971741164361", 
       "name": "Purmerend, Purmerend, Jan Blankenbrug", 
       "id": "37400060"
     }, 
     {
       "lat": "4.94879905636499", 
       "lon": "52.4966119597691", 
       "name": "Purmerend, Purmerend, Jan Blankenbrug", 
       "id": "37400061"
     }, 
     {
       "lat": "4.94593875937522", 
       "lon": "52.5028655999492", 
       "name": "Purmerend, Purmerend, Rozenstraat", 
       "id": "37400080"
     }, 
     {
       "lat": "4.95719970322659", 
       "lon": "52.5125324638522", 
       "name": "Purmerend, Purmerend, Wormerplein", 
       "id": "37400090"
     }, 
     {
       "lat": "4.94454119078663", 
       "lon": "52.5071204349692", 
       "name": "Purmerend, Purmerend, Tramplein", 
       "id": "37400101"
     }, 
     {
       "lat": "4.94454119078663", 
       "lon": "52.5071204349692", 
       "name": "Purmerend, Purmerend, Tramplein", 
       "id": "37400102"
     }, 
     {
       "lat": "4.944407012843", 
       "lon": "52.5072817079806", 
       "name": "Purmerend, Purmerend, Tramplein", 
       "id": "37400104"
     }, 
     {
       "lat": "4.94439075303077", 
       "lon": "52.5074344334905", 
       "name": "Purmerend, Purmerend, Tramplein", 
       "id": "37400106"
     }, 
     {
       "lat": "4.94417009398267", 
       "lon": "52.5074066476173", 
       "name": "Purmerend, Purmerend, Tramplein", 
       "id": "37400107"
     }, 
     {
       "lat": "4.944187255687", 
       "lon": "52.5071640512721", 
       "name": "Purmerend, Purmerend, Tramplein", 
       "id": "37400108"
     }, 
     {
       "lat": "4.94421887533451", 
       "lon": "52.5069484711551", 
       "name": "Purmerend, Purmerend, Tramplein", 
       "id": "37400109"
     }, 
     {
       "lat": "4.94830874788112", 
       "lon": "52.5074310141385", 
       "name": "Purmerend, Purmerend, Liduinatuin", 
       "id": "37400120"
     }, 
     {
       "lat": "4.95474797905169", 
       "lon": "52.5071670576396", 
       "name": "Purmerend, Purmerend, Stadhuis", 
       "id": "37400130"
     }, 
     {
       "lat": "4.95383357463879", 
       "lon": "52.5072895456448", 
       "name": "Purmerend, Purmerend, Stadhuis", 
       "id": "37400140"
     }, 
     {
       "lat": "4.94829250150305", 
       "lon": "52.5075837401929", 
       "name": "Purmerend, Purmerend, Liduinatuin", 
       "id": "37400150"
     }, 
     {
       "lat": "4.95728607368222", 
       "lon": "52.5127394870837", 
       "name": "Purmerend, Purmerend, Wormerplein", 
       "id": "37400180"
     }, 
     {
       "lat": "4.94773020638151", 
       "lon": "52.4959968594061", 
       "name": "Purmerend, Purmerend, Jan Blankenbrug", 
       "id": "37400190"
     }, 
     {
       "lat": "4.94933653454696", 
       "lon": "52.4914102130036", 
       "name": "Purmerend, Purmerend, Vurige Staart", 
       "id": "37400210"
     }, 
     {
       "lat": "4.95743467495423", 
       "lon": "52.5216914716105", 
       "name": "Purmerend, Purmerend, Sternstraat", 
       "id": "37400220"
     }, 
     {
       "lat": "4.95770572650111", 
       "lon": "52.5104851673816", 
       "name": "Purmerend, Purmerend, Doplaan", 
       "id": "37400230"
     }, 
     {
       "lat": "4.95783733270189", 
       "lon": "52.5105845051081", 
       "name": "Purmerend, Purmerend, Doplaan", 
       "id": "37400240"
     }, 
     {
       "lat": "4.96302730230579", 
       "lon": "52.5238775483363", 
       "name": "Purmerend, Purmerend, M.L. Kingweg", 
       "id": "37400260"
     }, 
     {
       "lat": "4.96510928351783", 
       "lon": "52.5234176263089", 
       "name": "Purmerend, Purmerend, M.L. Kingweg", 
       "id": "37400261"
     }, 
     {
       "lat": "4.96841121686677", 
       "lon": "52.4952987410357", 
       "name": "Purmerend, Purmerend, Delfland", 
       "id": "37400270"
     }, 
     {
       "lat": "4.96896684048972", 
       "lon": "52.4957141228813", 
       "name": "Purmerend, Purmerend, Delfland", 
       "id": "37400280"
     }, 
     {
       "lat": "4.96996756749945", 
       "lon": "52.4942167447689", 
       "name": "Purmerend, Purmerend, Winkelcentrum Meerland", 
       "id": "37400290"
     }, 
     {
       "lat": "4.96887320903026", 
       "lon": "52.4947161876053", 
       "name": "Purmerend, Purmerend, Winkelcentrum Meerland", 
       "id": "37400300"
     }, 
     {
       "lat": "4.97107188064679", 
       "lon": "52.4895291796578", 
       "name": "Purmerend, Purmerend, Frescobaldistraat", 
       "id": "37400310"
     }, 
     {
       "lat": "4.97234482772554", 
       "lon": "52.4903784574776", 
       "name": "Purmerend, Purmerend, Frescobaldistraat", 
       "id": "37400320"
     }, 
     {
       "lat": "4.9684082710692", 
       "lon": "52.487839154138", 
       "name": "Purmerend, Purmerend, Beethovenstraat", 
       "id": "37400350"
     }, 
     {
       "lat": "4.98934951027189", 
       "lon": "52.506838737547", 
       "name": "Purmerend, Purmerend, Tarwestraat", 
       "id": "37400410"
     }, 
     {
       "lat": "4.97823671036618", 
       "lon": "52.4964744188284", 
       "name": "Purmerend, Purmerend, IJsselmeerlaan", 
       "id": "37400420"
     }, 
     {
       "lat": "4.98756609529376", 
       "lon": "52.5020873944952", 
       "name": "Purmerend, Purmerend, Bunderstraat", 
       "id": "37400430"
     }, 
     {
       "lat": "4.9857875357022", 
       "lon": "52.5000861852916", 
       "name": "Purmerend, Purmerend, Zuivelpad", 
       "id": "37400440"
     }, 
     {
       "lat": "4.98524609797736", 
       "lon": "52.4997068808888", 
       "name": "Purmerend, Purmerend, Zuivelpad", 
       "id": "37400450"
     }, 
     {
       "lat": "4.98774273698486", 
       "lon": "52.5020969766795", 
       "name": "Purmerend, Purmerend, Bunderstraat", 
       "id": "37400460"
     }, 
     {
       "lat": "4.97709533010899", 
       "lon": "52.4956975603624", 
       "name": "Purmerend, Purmerend, IJsselmeerlaan", 
       "id": "37400470"
     }, 
     {
       "lat": "4.98987908967983", 
       "lon": "52.5069124110206", 
       "name": "Purmerend, Purmerend, Tarwestraat", 
       "id": "37400480"
     }, 
     {
       "lat": "4.95899170346849", 
       "lon": "52.5039469762695", 
       "name": "Purmerend, Purmerend, Waterlandplein", 
       "id": "37400520"
     }, 
     {
       "lat": "4.98671974246561", 
       "lon": "52.5109730823941", 
       "name": "Purmerend, Purmerend, De Graeffweg", 
       "id": "37400530"
     }, 
     {
       "lat": "4.96245599167413", 
       "lon": "52.5020810559702", 
       "name": "Purmerend, Purmerend, Waterlandlaan", 
       "id": "37400540"
     }, 
     {
       "lat": "4.98365183647622", 
       "lon": "52.5081855840082", 
       "name": "Purmerend, Purmerend, Zichthof", 
       "id": "37400550"
     }, 
     {
       "lat": "4.98404236551557", 
       "lon": "52.5057423377075", 
       "name": "Purmerend, Purmerend, Gildeplein", 
       "id": "37400570"
     }, 
     {
       "lat": "4.98146404155977", 
       "lon": "52.5026239063051", 
       "name": "Purmerend, Purmerend, Hoefsmidpad", 
       "id": "37400580"
     }, 
     {
       "lat": "4.98242549169932", 
       "lon": "52.5037775785433", 
       "name": "Purmerend, Purmerend, Wijkcentrum", 
       "id": "37400590"
     }, 
     {
       "lat": "4.98289397484424", 
       "lon": "52.5040847475982", 
       "name": "Purmerend, Purmerend, Wijkcentrum", 
       "id": "37400600"
     }, 
     {
       "lat": "4.98093733692229", 
       "lon": "52.5022446328088", 
       "name": "Purmerend, Purmerend, Hoefsmidpad", 
       "id": "37400610"
     }, 
     {
       "lat": "4.9839934245252", 
       "lon": "52.5062634409239", 
       "name": "Purmerend, Purmerend, Gildeplein", 
       "id": "37400620"
     }, 
     {
       "lat": "4.98450373949318", 
       "lon": "52.5084491124763", 
       "name": "Purmerend, Purmerend, Zichthof", 
       "id": "37400640"
     }, 
     {
       "lat": "4.98666693389181", 
       "lon": "52.5102988495884", 
       "name": "Purmerend, Purmerend, De Graeffweg", 
       "id": "37400660"
     }, 
     {
       "lat": "4.95830603920254", 
       "lon": "52.5047893175531", 
       "name": "Purmerend, Purmerend, Waterlandplein", 
       "id": "37400670"
     }, 
     {
       "lat": "4.99086345811858", 
       "lon": "52.5088300184906", 
       "name": "Purmerend, Purmerend, Boekweitstraat", 
       "id": "37400680"
     }, 
     {
       "lat": "4.95551610537255", 
       "lon": "52.5039253956616", 
       "name": "Purmerend, Purmerend, Beatrixplein", 
       "id": "37400700"
     }, 
     {
       "lat": "4.95586053974949", 
       "lon": "52.5033424656441", 
       "name": "Purmerend, Purmerend, Beatrixplein", 
       "id": "37400710"
     }, 
     {
       "lat": "4.95547244980272", 
       "lon": "52.5038713122942", 
       "name": "Purmerend, Purmerend, Beatrixplein", 
       "id": "37400720"
     }, 
     {
       "lat": "4.9502056923542", 
       "lon": "52.5092354983615", 
       "name": "Purmerend, Purmerend, Gedempte Where", 
       "id": "37400730"
     }, 
     {
       "lat": "4.94900415605339", 
       "lon": "52.5100848721842", 
       "name": "Purmerend, Purmerend, Gedempte Where", 
       "id": "37400740"
     }, 
     {
       "lat": "4.97435403996482", 
       "lon": "52.4975304762857", 
       "name": "Purmerend, Purmerend, Slotermeer", 
       "id": "37400750"
     }, 
     {
       "lat": "4.97371975595776", 
       "lon": "52.4976451041446", 
       "name": "Purmerend, Purmerend, Slotermeer", 
       "id": "37400760"
     }, 
     {
       "lat": "4.97371436361977", 
       "lon": "52.4966474808627", 
       "name": "Purmerend, Purmerend, Slotermeer", 
       "id": "37400770"
     }, 
     {
       "lat": "4.95829179311986", 
       "lon": "52.500187704461", 
       "name": "Purmerend, Purmerend, Weteringstraat", 
       "id": "37400780"
     }, 
     {
       "lat": "4.96539753440686", 
       "lon": "52.5009501461755", 
       "name": "Purmerend, Purmerend, Basisveenstraat", 
       "id": "37400800"
     }, 
     {
       "lat": "4.96475982759258", 
       "lon": "52.5014152235863", 
       "name": "Purmerend, Purmerend, Basisveenstraat", 
       "id": "37400810"
     }, 
     {
       "lat": "4.96757917841717", 
       "lon": "52.4976325336269", 
       "name": "Purmerend, Purmerend, Landstrekenweg", 
       "id": "37400820"
     }, 
     {
       "lat": "4.96806375279309", 
       "lon": "52.497778045267", 
       "name": "Purmerend, Purmerend, Landstrekenweg", 
       "id": "37400830"
     }, 
     {
       "lat": "4.96989276322002", 
       "lon": "52.4974609447604", 
       "name": "Purmerend, Purmerend, Salland", 
       "id": "37400840"
     }, 
     {
       "lat": "4.96926390787277", 
       "lon": "52.4970003724048", 
       "name": "Purmerend, Purmerend, Salland", 
       "id": "37400850"
     }, 
     {
       "lat": "4.96526195098854", 
       "lon": "52.495098846974", 
       "name": "Purmerend, Purmerend, Mergelland", 
       "id": "37400860"
     }, 
     {
       "lat": "4.96644521929099", 
       "lon": "52.4945458280975", 
       "name": "Purmerend, Purmerend, Mergelland", 
       "id": "37400870"
     }, 
     {
       "lat": "4.96247508244831", 
       "lon": "52.4970301893738", 
       "name": "Purmerend, Purmerend, Bovenlandsestraat", 
       "id": "37400880"
     }, 
     {
       "lat": "4.96228365501979", 
       "lon": "52.4970295039677", 
       "name": "Purmerend, Purmerend, Bovenlandsestraat", 
       "id": "37400890"
     }, 
     {
       "lat": "4.96071591606023", 
       "lon": "52.4992617497218", 
       "name": "Purmerend, Purmerend, Veenweidestraat/Waterlandziekenhuis", 
       "id": "37400900"
     }, 
     {
       "lat": "4.95984439223053", 
       "lon": "52.4995372242579", 
       "name": "Purmerend, Purmerend, Veenweidestraat/Waterlandziekenhuis", 
       "id": "37400910"
     }, 
     {
       "lat": "4.95954213370304", 
       "lon": "52.4957704003753", 
       "name": "Purmerend, Purmerend, Dijckscampenlaan", 
       "id": "37400920"
     }, 
     {
       "lat": "4.95960416286315", 
       "lon": "52.495447076174", 
       "name": "Purmerend, Purmerend, Dijckscampenlaan", 
       "id": "37400930"
     }, 
     {
       "lat": "4.95858607850262", 
       "lon": "52.492621345947", 
       "name": "Purmerend, Purmerend, Lepelblad", 
       "id": "37400940"
     }, 
     {
       "lat": "4.95852631206828", 
       "lon": "52.4927110044556", 
       "name": "Purmerend, Purmerend, Lepelblad", 
       "id": "37400950"
     }, 
     {
       "lat": "4.95367840583257", 
       "lon": "52.4900780409201", 
       "name": "Purmerend, Purmerend, Fonteinkruid", 
       "id": "37400960"
     }, 
     {
       "lat": "4.95345712207259", 
       "lon": "52.4901221693429", 
       "name": "Purmerend, Purmerend, Fonteinkruid", 
       "id": "37400970"
     }, 
     {
       "lat": "4.98125950079208", 
       "lon": "52.4976351896552", 
       "name": "Purmerend, Purmerend, Sjeesstraat", 
       "id": "37401010"
     }, 
     {
       "lat": "4.9809657359176", 
       "lon": "52.49755329743", 
       "name": "Purmerend, Purmerend, Sjeesstraat", 
       "id": "37401040"
     }, 
     {
       "lat": "4.9737706177125", 
       "lon": "52.4922078848837", 
       "name": "Purmerend, Purmerend, Mastbos", 
       "id": "37401050"
     }, 
     {
       "lat": "4.97343845433871", 
       "lon": "52.4930874957385", 
       "name": "Purmerend, Purmerend, Mastbos", 
       "id": "37401080"
     }, 
     {
       "lat": "4.96270214375028", 
       "lon": "52.4902544719463", 
       "name": "Purmerend, Purmerend, Cornelis Edelmanstraat", 
       "id": "37401090"
     }, 
     {
       "lat": "4.96270214375028", 
       "lon": "52.4902544719463", 
       "name": "Purmerend, Purmerend, Cornelis Edelmanstraat", 
       "id": "37401091"
     }, 
     {
       "lat": "4.96346808072816", 
       "lon": "52.4902212603381", 
       "name": "Purmerend, Purmerend, Cornelis Edelmanstraat", 
       "id": "37401120"
     }, 
     {
       "lat": "4.96995316226298", 
       "lon": "52.4879434597612", 
       "name": "Purmerend, Purmerend, Beethovenstraat/Verzetslaan", 
       "id": "37401140"
     }, 
     {
       "lat": "4.97493978838167", 
       "lon": "52.4931466467126", 
       "name": "Purmerend, Purmerend, Mastbos", 
       "id": "37401155"
     }, 
     {
       "lat": "4.97422604167249", 
       "lon": "52.4923173202835", 
       "name": "Purmerend, Purmerend, Mastbos", 
       "id": "37401160"
     }, 
     {
       "lat": "4.96016492431282", 
       "lon": "52.4877019175986", 
       "name": "Purmerend, Purmerend, Moeder Teresastraat", 
       "id": "37401170"
     }, 
     {
       "lat": "4.95889359468629", 
       "lon": "52.4867177017626", 
       "name": "Purmerend, Purmerend, Moeder Teresastraat", 
       "id": "37401180"
     }, 
     {
       "lat": "4.95858731337183", 
       "lon": "52.486420009478", 
       "name": "Purmerend, Purmerend, Moeder Teresastraat", 
       "id": "37401181"
     }, 
     {
       "lat": "4.9666141055883", 
       "lon": "52.4845344115238", 
       "name": "Purmerend, Purmerend, Dom Helder Camarastraat", 
       "id": "37401220"
     }, 
     {
       "lat": "4.95249061938991", 
       "lon": "52.4970749147164", 
       "name": "Purmerend, Purmerend, Linnaeuslaan", 
       "id": "37401450"
     }, 
     {
       "lat": "4.97811375401869", 
       "lon": "52.4986219894984", 
       "name": "Purmerend, Purmerend, Tilburyplein", 
       "id": "37401510"
     }, 
     {
       "lat": "4.96127030577549", 
       "lon": "52.5028587116508", 
       "name": "Purmerend, Purmerend, Waterlandlaan", 
       "id": "37401520"
     }, 
     {
       "lat": "4.96132150306281", 
       "lon": "52.5021309141152", 
       "name": "Purmerend, Purmerend, Waterlandlaan", 
       "id": "37401530"
     }, 
     {
       "lat": "4.95823960538063", 
       "lon": "52.4994954836684", 
       "name": "Purmerend, Purmerend, Veenweidestraat", 
       "id": "37401550"
     }, 
     {
       "lat": "4.95958683216105", 
       "lon": "52.5002822529633", 
       "name": "Purmerend, Purmerend, Veenweidestraat", 
       "id": "37401560"
     }, 
     {
       "lat": "4.95084104384742", 
       "lon": "52.4971048091608", 
       "name": "Purmerend, Purmerend, Linnaeuslaan", 
       "id": "37401570"
     }, 
     {
       "lat": "4.97842183082194", 
       "lon": "52.4987488751831", 
       "name": "Purmerend, Purmerend, Tilburyplein", 
       "id": "37401580"
     }, 
     {
       "lat": "4.9709641625147", 
       "lon": "52.4947145541857", 
       "name": "Purmerend, Purmerend, Grevelingenmeer", 
       "id": "37401610"
     }, 
     {
       "lat": "4.97140335903526", 
       "lon": "52.4949857171893", 
       "name": "Purmerend, Purmerend, Grevelingenmeer", 
       "id": "37401620"
     }, 
     {
       "lat": "4.96964133988845", 
       "lon": "52.5209531388437", 
       "name": "Purmerend, Purmerend, Koogsingel", 
       "id": "37402010"
     }, 
     {
       "lat": "4.96341362097087", 
       "lon": "52.5189358668156", 
       "name": "Purmerend, Purmerend, Prof.Mr.P.J.Oudlaan", 
       "id": "37402030"
     }, 
     {
       "lat": "4.96262537443803", 
       "lon": "52.5028455931062", 
       "name": "Purmerend, Purmerend, Waterlandlaan", 
       "id": "37402040"
     }, 
     {
       "lat": "4.96428288956385", 
       "lon": "52.5158562919112", 
       "name": "Purmerend, Purmerend, Flevostraat", 
       "id": "37402050"
     }, 
     {
       "lat": "4.9646267475875", 
       "lon": "52.5045513595724", 
       "name": "Purmerend, Purmerend, Brug Wheermolen", 
       "id": "37402060"
     }, 
     {
       "lat": "4.96531801926828", 
       "lon": "52.5123638780818", 
       "name": "Purmerend, Purmerend, van IJsendijkstraat", 
       "id": "37402070"
     }, 
     {
       "lat": "4.96783877984911", 
       "lon": "52.5075196134038", 
       "name": "Purmerend, Purmerend, Churchilllaan", 
       "id": "37402080"
     }, 
     {
       "lat": "4.96670727064886", 
       "lon": "52.5103376554541", 
       "name": "Purmerend, Purmerend, Meteorenweg/NS", 
       "id": "37402090"
     }, 
     {
       "lat": "4.97251528451348", 
       "lon": "52.5067361680333", 
       "name": "Purmerend, Purmerend, Hannie Schaftstraat", 
       "id": "37402100"
     }, 
     {
       "lat": "4.97099799745528", 
       "lon": "52.5098854360044", 
       "name": "Purmerend, Purmerend, Anne Franklaan", 
       "id": "37402110"
     }, 
     {
       "lat": "4.97456006000386", 
       "lon": "52.5085857141777", 
       "name": "Purmerend, Purmerend, Albert Schweitzerlaan", 
       "id": "37402120"
     }, 
     {
       "lat": "4.9740474844337", 
       "lon": "52.5082693715875", 
       "name": "Purmerend, Purmerend, Albert Schweitzerlaan", 
       "id": "37402130"
     }, 
     {
       "lat": "4.97087922998485", 
       "lon": "52.5099838808555", 
       "name": "Purmerend, Purmerend, Anne Franklaan", 
       "id": "37402140"
     }, 
     {
       "lat": "4.96985627151811", 
       "lon": "52.507562675441", 
       "name": "Purmerend, Purmerend, Hannie Schaftstraat", 
       "id": "37402150"
     }, 
     {
       "lat": "4.96698610784437", 
       "lon": "52.5104464919734", 
       "name": "Purmerend, Purmerend, Meteorenweg/NS", 
       "id": "37402160"
     }, 
     {
       "lat": "4.96766041411427", 
       "lon": "52.5076897437378", 
       "name": "Purmerend, Purmerend, Churchilllaan", 
       "id": "37402170"
     }, 
     {
       "lat": "4.96527877341791", 
       "lon": "52.5133883022326", 
       "name": "Purmerend, Purmerend, van IJsendijkstraat", 
       "id": "37402180"
     }, 
     {
       "lat": "4.96316208512916", 
       "lon": "52.5037013172809", 
       "name": "Purmerend, Purmerend, Brug Wheermolen", 
       "id": "37402190"
     }, 
     {
       "lat": "4.96421200114994", 
       "lon": "52.5171052870407", 
       "name": "Purmerend, Purmerend, Flevostraat", 
       "id": "37402200"
     }, 
     {
       "lat": "4.96474774511536", 
       "lon": "52.5196236643193", 
       "name": "Purmerend, Purmerend, Prof.Mr.P.J.Oudlaan", 
       "id": "37402220"
     }, 
     {
       "lat": "4.97032557074574", 
       "lon": "52.5218273198843", 
       "name": "Purmerend, Purmerend, Koogsingel", 
       "id": "37402240"
     }, 
     {
       "lat": "4.95255715132366", 
       "lon": "52.4873147894447", 
       "name": "Purmerend, Purmerend, Klaverblad", 
       "id": "37402250"
     }, 
     {
       "lat": "4.97306140488287", 
       "lon": "52.5176128268984", 
       "name": "Purmerend, Purmerend, Cantekoogweg", 
       "id": "37402262"
     }, 
     {
       "lat": "4.97269478999348", 
       "lon": "52.5174317993603", 
       "name": "Purmerend, Purmerend, Cantekoogweg", 
       "id": "37402263"
     }, 
     {
       "lat": "4.96472405033409", 
       "lon": "52.52364094029", 
       "name": "Purmerend, Purmerend, M.L. Kingweg", 
       "id": "37402520"
     }, 
     {
       "lat": "4.99447518021775", 
       "lon": "52.5151242098602", 
       "name": "Purmerend, Purmerend, Kelvinstraat", 
       "id": "37402540"
     }, 
     {
       "lat": "4.99974905552038", 
       "lon": "52.5151325560691", 
       "name": "Purmerend, Purmerend, Amperestraat", 
       "id": "37402550"
     }, 
     {
       "lat": "5.00072952522871", 
       "lon": "52.5158817051048", 
       "name": "Purmerend, Purmerend, Amperestraat", 
       "id": "37402560"
     }, 
     {
       "lat": "4.99534065782564", 
       "lon": "52.5155404900208", 
       "name": "Purmerend, Purmerend, Kelvinstraat", 
       "id": "37402570"
     }, 
     {
       "lat": "4.94510811042515", 
       "lon": "52.496094967304", 
       "name": "Purmerend, Purmerend, Azielaan", 
       "id": "37403010"
     }, 
     {
       "lat": "4.94315006720788", 
       "lon": "52.4960517053301", 
       "name": "Purmerend, Purmerend, Azielaan", 
       "id": "37403100"
     }, 
     {
       "lat": "4.944169503938", 
       "lon": "52.4957139934585", 
       "name": "Purmerend, Purmerend, Azielaan", 
       "id": "37403110"
     }, 
     {
       "lat": "4.94555776486183", 
       "lon": "52.4923578635327", 
       "name": "Purmerend, Purmerend, Eufraatlaan", 
       "id": "37403200"
     }, 
     {
       "lat": "4.94466241445417", 
       "lon": "52.4920759160778", 
       "name": "Purmerend, Purmerend, Eufraatlaan", 
       "id": "37403300"
     }, 
     {
       "lat": "4.93226041169414", 
       "lon": "52.4996503651961", 
       "name": "Purmerend, Purmerend, Savannestraat", 
       "id": "37403500"
     }, 
     {
       "lat": "4.93345174235658", 
       "lon": "52.4997987262228", 
       "name": "Purmerend, Purmerend, Savannestraat", 
       "id": "37403600"
     }, 
     {
       "lat": "4.93984748548512", 
       "lon": "52.5008206183607", 
       "name": "Purmerend, Purmerend, Retiropark", 
       "id": "37403620"
     }, 
     {
       "lat": "4.94209945062382", 
       "lon": "52.5009459241365", 
       "name": "Purmerend, Purmerend, Retiropark", 
       "id": "37403630"
     }, 
     {
       "lat": "4.93866443475218", 
       "lon": "52.5042044151713", 
       "name": "Purmerend, Purmerend, Vallettastraat", 
       "id": "37403660"
     }, 
     {
       "lat": "4.93888480075939", 
       "lon": "52.5042591725454", 
       "name": "Purmerend, Purmerend, Vallettastraat", 
       "id": "37403670"
     }, 
     {
       "lat": "4.94075977591997", 
       "lon": "52.5067287970128", 
       "name": "Purmerend, Purmerend, Vuurtorengracht", 
       "id": "37403680"
     }, 
     {
       "lat": "4.94064403800471", 
       "lon": "52.5065216507283", 
       "name": "Purmerend, Purmerend, Vuurtorengracht", 
       "id": "37403690"
     }, 
     {
       "lat": "4.93510631526388", 
       "lon": "52.4920938098078", 
       "name": "Purmerend, Purmerend, Woestijnstraat", 
       "id": "37403880"
     }, 
     {
       "lat": "4.93515232398666", 
       "lon": "52.491914235965", 
       "name": "Purmerend, Purmerend, Woestijnstraat", 
       "id": "37403890"
     }, 
     {
       "lat": "4.9388986414523", 
       "lon": "52.4912813548051", 
       "name": "Purmerend, Purmerend, Karavaanstraat", 
       "id": "37403900"
     }, 
     {
       "lat": "4.93937197017684", 
       "lon": "52.4910674435112", 
       "name": "Purmerend, Purmerend, Karavaanstraat", 
       "id": "37403910"
     }, 
     {
       "lat": "4.93123348047459", 
       "lon": "52.4921329128783", 
       "name": "Purmerend, Purmerend, Zoeloestraat", 
       "id": "37403920"
     }, 
     {
       "lat": "4.93129459920103", 
       "lon": "52.4919174487232", 
       "name": "Purmerend, Purmerend, Zoeloestraat", 
       "id": "37403930"
     }, 
     {
       "lat": "4.92916811931101", 
       "lon": "52.4967804593282", 
       "name": "Purmerend, Purmerend, Orinocostraat", 
       "id": "37403940"
     }, 
     {
       "lat": "4.92873252099385", 
       "lon": "52.4961856050016", 
       "name": "Purmerend, Purmerend, Orinocostraat", 
       "id": "37403950"
     }, 
     {
       "lat": "4.91941694234229", 
       "lon": "52.5081744449227", 
       "name": "Neck, Neck, Neckerbrug", 
       "id": "37404010"
     }, 
     {
       "lat": "4.94208705214465", 
       "lon": "52.5109488834273", 
       "name": "Purmerend, Purmerend, Sluisbrug", 
       "id": "37404020"
     }, 
     {
       "lat": "4.93475962692956", 
       "lon": "52.5101392680513", 
       "name": "Purmerend, Purmerend, Graanmaalderij", 
       "id": "37404030"
     }, 
     {
       "lat": "4.93503691214631", 
       "lon": "52.5103919727077", 
       "name": "Purmerend, Purmerend, Graanmaalderij", 
       "id": "37404040"
     }, 
     {
       "lat": "4.94192429972221", 
       "lon": "52.5110201722033", 
       "name": "Purmerend, Purmerend, Sluisbrug", 
       "id": "37404050"
     }, 
     {
       "lat": "4.98544047817252", 
       "lon": "52.5204414623205", 
       "name": "Purmerend, Purmerend, Nieuwe Gouw", 
       "id": "37405010"
     }, 
     {
       "lat": "4.98137660672671", 
       "lon": "52.5185582625141", 
       "name": "Purmerend, Purmerend, Kwadijkerkoogweg", 
       "id": "37405030"
     }, 
     {
       "lat": "4.98181915598431", 
       "lon": "52.5184968631585", 
       "name": "Purmerend, Purmerend, Kwadijkerkoogweg", 
       "id": "37405080"
     }, 
     {
       "lat": "4.98582116840586", 
       "lon": "52.5207033841361", 
       "name": "Purmerend, Purmerend, Nieuwe Gouw", 
       "id": "37405100"
     }, 
     {
       "lat": "4.9616559518429", 
       "lon": "52.5193969222699", 
       "name": "Purmerend, Purmerend, Prof.Mr.P.J.Oudlaan", 
       "id": "37405110"
     }, 
     {
       "lat": "4.96431960401359", 
       "lon": "52.5243315282515", 
       "name": "Purmerend, Purmerend, S.Allendeln/M.L.Kingweg", 
       "id": "37405180"
     }, 
     {
       "lat": "5.00624802741627", 
       "lon": "52.513158395727", 
       "name": "Purmerend, Purmerend, Signaal", 
       "id": "37405250"
     }, 
     {
       "lat": "5.00723899912158", 
       "lon": "52.5126942286174", 
       "name": "Purmerend, Purmerend, Signaal", 
       "id": "37405260"
     }, 
     {
       "lat": "5.00972900062454", 
       "lon": "52.5109136852106", 
       "name": "Purmerend, Purmerend, Magneet", 
       "id": "37405270"
     }, 
     {
       "lat": "5.01003104056509", 
       "lon": "52.5100428692392", 
       "name": "Purmerend, Purmerend, Magneet", 
       "id": "37405280"
     }, 
     {
       "lat": "5.00160686124213", 
       "lon": "52.513260243772", 
       "name": "Purmerend, Purmerend, Westerweg", 
       "id": "37405310"
     }, 
     {
       "lat": "5.0027461274856", 
       "lon": "52.5126887471996", 
       "name": "Purmerend, Purmerend, Westerweg", 
       "id": "37405320"
     }, 
     {
       "lat": "4.96325908876085", 
       "lon": "52.5012660723975", 
       "name": "Purmerend, Purmerend, Waterlandziekenhuis", 
       "id": "37405330"
     }, 
     {
       "lat": "4.96325908876085", 
       "lon": "52.5012660723975", 
       "name": "Purmerend, Purmerend, Waterlandziekenhuis", 
       "id": "37405340"
     }, 
     {
       "lat": "4.96487505691066", 
       "lon": "52.5047679415871", 
       "name": "t.h.v. Brug Wheermolen, t.h.v. Brug Wheermolen", 
       "id": "37409609"
     }, 
     {
       "lat": "4.96313297530469", 
       "lon": "52.5036652635723", 
       "name": "t.h.v. Brug Wheermolen, t.h.v. Brug Wheermolen", 
       "id": "37409619"
     }, 
     {
       "lat": "4.95790742690499", 
       "lon": "52.5003391007418", 
       "name": "t.h.v. Kruising Gorslaan, t.h.v. Kruising Gorslaan", 
       "id": "37409629"
     }, 
     {
       "lat": "4.92904518505425", 
       "lon": "52.4944342590996", 
       "name": "t.h.v. Busbaan Spoor, t.h.v. Busbaan Spoor", 
       "id": "37409639"
     }, 
     {
       "lat": "4.92921246017682", 
       "lon": "52.4939226199009", 
       "name": "t.h.v. Busbaan Spoor, t.h.v. Busbaan Spoor", 
       "id": "37409649"
     }, 
     {
       "lat": "4.95961602382419", 
       "lon": "52.5003093204484", 
       "name": "t.h.v. Kruising Gorslaan, t.h.v. Kruising Gorslaan", 
       "id": "37409679"
     }, 
     {
       "lat": "4.9787936039034", 
       "lon": "52.4967639346813", 
       "name": "t.h.v. IJsselmeerlaan, t.h.v. IJsselmeerlaan", 
       "id": "37409689"
     }, 
     {
       "lat": "4.97654096618771", 
       "lon": "52.495138422258", 
       "name": "t.h.v. IJsselmeerlaan, t.h.v. IJsselmeerlaan", 
       "id": "37409699"
     }, 
     {
       "lat": "4.94535707273414", 
       "lon": "52.5315781852901", 
       "name": "t.h.v. Kruising A7, t.h.v. Kruising A7", 
       "id": "37409709"
     }, 
     {
       "lat": "4.95283506089731", 
       "lon": "52.5294488132916", 
       "name": "t.h.v. Kruising A7, t.h.v. Kruising A7", 
       "id": "37409719"
     }, 
     {
       "lat": "4.95991871746973", 
       "lon": "52.4994655924931", 
       "name": "t.h.v. Kruising Gorslaan, t.h.v. Kruising Gorslaan", 
       "id": "37409739"
     }, 
     {
       "lat": "4.98630311932013", 
       "lon": "52.5211723563486", 
       "name": "t.h.v. Kruising N244, t.h.v. Kruising N244", 
       "id": "37409749"
     }, 
     {
       "lat": "4.98617011182652", 
       "lon": "52.5212168439126", 
       "name": "t.h.v. Kruising N244, t.h.v. Kruising N244", 
       "id": "37409759"
     }, 
     {
       "lat": "4.97458905859476", 
       "lon": "52.4975942057877", 
       "name": "t.h.v. Viadukt IJsselmeerlaan, t.h.v. Viadukt IJsselmeerlaan", 
       "id": "37409779"
     }, 
     {
       "lat": "4.96659808835221", 
       "lon": "52.5109753742566", 
       "name": "t.h.v. Spoorwegovergang, t.h.v. Spoorwegovergang", 
       "id": "37409799"
     }, 
     {
       "lat": "4.96688676230552", 
       "lon": "52.5100506943362", 
       "name": "t.h.v. Spoorwegovergang, t.h.v. Spoorwegovergang", 
       "id": "37409809"
     }, 
     {
       "lat": "4.94452205002706", 
       "lon": "52.50756074727", 
       "name": "t.h.v. Tramplein ingang Noord, t.h.v. Tramplein ingang Noord", 
       "id": "37409819"
     }, 
     {
       "lat": "4.94417685270605", 
       "lon": "52.5067326161072", 
       "name": "t.h.v. Tramplein ingang Zuid, t.h.v. Tramplein ingang Zuid", 
       "id": "37409829"
     }, 
     {
       "lat": "4.94418103773738", 
       "lon": "52.5077841602061", 
       "name": "t.h.v. Tramplein uitgang Noord, t.h.v. Tramplein uitgang Noord", 
       "id": "37409839"
     }, 
     {
       "lat": "4.94399073609628", 
       "lon": "52.5076666131144", 
       "name": "t.h.v. Tramplein uitgang Noord, t.h.v. Tramplein uitgang Noord", 
       "id": "37409849"
     }, 
     {
       "lat": "4.94430850736262", 
       "lon": "52.5068229817906", 
       "name": "t.h.v. Tramplein uitgang Zuid, t.h.v. Tramplein uitgang Zuid", 
       "id": "37409859"
     }, 
     {
       "lat": "4.95819595083555", 
       "lon": "52.4994414012513", 
       "name": "t.h.v. Kruising Gorslaan, t.h.v. Kruising Gorslaan", 
       "id": "37409869"
     }, 
     {
       "lat": "4.97534975415168", 
       "lon": "52.4981360942191", 
       "name": "t.h.v. IJsselmeerlaan, t.h.v. IJsselmeerlaan", 
       "id": "37409879"
     }, 
     {
       "lat": "4.97514518815077", 
       "lon": "52.4979646228969", 
       "name": "t.h.v. IJsselmeerlaan, t.h.v. IJsselmeerlaan", 
       "id": "37409889"
     }, 
     {
       "lat": "4.95897355423455", 
       "lon": "52.4997407954354", 
       "name": "t.h.v. kruising Gorslaan, t.h.v. kruising Gorslaan", 
       "id": "37409899"
     }, 
     {
       "lat": "4.97378134778054", 
       "lon": "52.4973577210996", 
       "name": "t.h.v. Viadukt IJsselmeerlaan, t.h.v. Viadukt IJsselmeerlaan", 
       "id": "37409909"
     }, 
     {
       "lat": "4.97391236286472", 
       "lon": "52.4975199512178", 
       "name": "t.h.v. Viadukt IJsselmeerlaan, t.h.v. Viadukt IJsselmeerlaan", 
       "id": "37409919"
     }, 
     {
       "lat": "4.84725156662348", 
       "lon": "52.5026103353344", 
       "name": "Wormer, Wormer, Keerlus Wormer - Oost", 
       "id": "37420020"
     }, 
     {
       "lat": "4.84262213899282", 
       "lon": "52.5018162528572", 
       "name": "Wormer, Wormer, Geugjes", 
       "id": "37420040"
     }, 
     {
       "lat": "4.83429646722329", 
       "lon": "52.5010138089901", 
       "name": "Wormer, Wormer, Raadhuis", 
       "id": "37420060"
     }, 
     {
       "lat": "4.82601231062168", 
       "lon": "52.5004446511663", 
       "name": "Wormer, Wormer, Mariastraat", 
       "id": "37420080"
     }, 
     {
       "lat": "4.81278479633633", 
       "lon": "52.4983861173871", 
       "name": "Wormer, Wormer, Zaandammerstraat", 
       "id": "37420090"
     }, 
     {
       "lat": "4.82161462167526", 
       "lon": "52.500001355274", 
       "name": "Wormer, Wormer, Koelemeyer", 
       "id": "37420100"
     }, 
     {
       "lat": "4.81627735945333", 
       "lon": "52.4993376778928", 
       "name": "Wormer, Wormer, Prins van Oranjestraat", 
       "id": "37420110"
     }, 
     {
       "lat": "4.81623155665478", 
       "lon": "52.4994632827021", 
       "name": "Wormer, Wormer, Prins van Oranjestraat", 
       "id": "37420120"
     }, 
     {
       "lat": "4.82139223685312", 
       "lon": "52.5001171325708", 
       "name": "Wormer, Wormer, Koelemeyer", 
       "id": "37420130"
     }, 
     {
       "lat": "4.82667601028283", 
       "lon": "52.5003669010812", 
       "name": "Wormer, Wormer, Mariastraat", 
       "id": "37420150"
     }, 
     {
       "lat": "4.8347951386417", 
       "lon": "52.5011779068461", 
       "name": "Wormer, Wormer, Raadhuis", 
       "id": "37420170"
     }, 
     {
       "lat": "4.842903272307", 
       "lon": "52.5017096929742", 
       "name": "Wormer, Wormer, Geugjes", 
       "id": "37420190"
     }, 
     {
       "lat": "4.81328046234013", 
       "lon": "52.4931038510555", 
       "name": "Wormer, Wormer, Waterzolder", 
       "id": "37420241"
     }, 
     {
       "lat": "4.81258343079762", 
       "lon": "52.4957517978164", 
       "name": "Wormer, Wormer, Spatterstraat", 
       "id": "37420251"
     }, 
     {
       "lat": "4.80706880066768", 
       "lon": "52.4907009265027", 
       "name": "Wormer, Wormer, De Balk", 
       "id": "37420261"
     }, 
     {
       "lat": "4.84583121126275", 
       "lon": "52.5019387887075", 
       "name": "t.h.v. Keerlus, t.h.v. Keerlus", 
       "id": "37429619"
     }, 
     {
       "lat": "4.8472378282152", 
       "lon": "52.502529385407", 
       "name": "t.h.v. Keerlus, t.h.v. Keerlus", 
       "id": "37429629"
     }, 
     {
       "lat": "5.109598348281", 
       "lon": "52.4619473640697", 
       "name": "Marken, Marken, Minneweg", 
       "id": "37470010"
     }, 
     {
       "lat": "5.109598348281", 
       "lon": "52.4619473640697", 
       "name": "Marken, Marken, Minneweg", 
       "id": "37470011"
     }, 
     {
       "lat": "5.0781725814468", 
       "lon": "52.4362103993681", 
       "name": "Uitdam, Uitdam, Aansluiting Markerdijk", 
       "id": "37470020"
     }, 
     {
       "lat": "5.10573100450557", 
       "lon": "52.4569412288963", 
       "name": "Marken, Marken, Kerkbuurt", 
       "id": "37470030"
     }, 
     {
       "lat": "5.10581950520855", 
       "lon": "52.4569054890997", 
       "name": "Marken, Marken, Kerkbuurt", 
       "id": "37470040"
     }, 
     {
       "lat": "5.03348900883659", 
       "lon": "52.4888239602678", 
       "name": "Katwoude, Katwoude, Hotel Volendam", 
       "id": "37490010"
     }, 
     {
       "lat": "5.03290211175959", 
       "lon": "52.4665243729088", 
       "name": "Katwoude, Katwoude, Lagedijk", 
       "id": "37490020"
     }, 
     {
       "lat": "5.0299079560719", 
       "lon": "52.4819558245421", 
       "name": "Katwoude, Katwoude, De Zedde", 
       "id": "37490030"
     }, 
     {
       "lat": "5.03030880775304", 
       "lon": "52.4833590703042", 
       "name": "Katwoude, Katwoude, De Zedde", 
       "id": "37490040"
     }, 
     {
       "lat": "5.02663206276322", 
       "lon": "52.5081981295357", 
       "name": "Edam, Edam, Oosterweg", 
       "id": "37500010"
     }, 
     {
       "lat": "5.02422215466554", 
       "lon": "52.5092962311477", 
       "name": "Edam, Edam, Oosterweg", 
       "id": "37500020"
     }, 
     {
       "lat": "4.99495463810816", 
       "lon": "52.5225134168973", 
       "name": "Kwadijk, Kwadijk, Stationsweg", 
       "id": "37500110"
     }, 
     {
       "lat": "4.99498306799817", 
       "lon": "52.5226303466047", 
       "name": "Kwadijk, Kwadijk, Stationsweg", 
       "id": "37500120"
     }, 
     {
       "lat": "5.01022515218675", 
       "lon": "52.5442583278704", 
       "name": "Middelie, Middelie, Klemweg", 
       "id": "37501050"
     }, 
     {
       "lat": "5.01038699647432", 
       "lon": "52.5442947908223", 
       "name": "Middelie, Middelie, Klemweg", 
       "id": "37501060"
     }, 
     {
       "lat": "5.01327061816999", 
       "lon": "52.5397473359381", 
       "name": "Middelie, Middelie, Harmonie", 
       "id": "37501070"
     }, 
     {
       "lat": "5.01344741625555", 
       "lon": "52.5397568799085", 
       "name": "Middelie, Middelie, Harmonie", 
       "id": "37501080"
     }, 
     {
       "lat": "5.01527373010969", 
       "lon": "52.536428316832", 
       "name": "Middelie, Middelie, Doopsgezinde Kerk", 
       "id": "37501090"
     }, 
     {
       "lat": "5.01543562556544", 
       "lon": "52.5364557858502", 
       "name": "Middelie, Middelie, Doopsgezinde Kerk", 
       "id": "37501100"
     }, 
     {
       "lat": "5.01688560632925", 
       "lon": "52.534033737826", 
       "name": "Middelie, Middelie, School", 
       "id": "37501110"
     }, 
     {
       "lat": "5.01704734331758", 
       "lon": "52.5340791788493", 
       "name": "Middelie, Middelie, School", 
       "id": "37501120"
     }, 
     {
       "lat": "5.01360719651994", 
       "lon": "52.531327265741", 
       "name": "Middelie, Middelie, Brink", 
       "id": "37501130"
     }, 
     {
       "lat": "5.01360810902262", 
       "lon": "52.5312194205292", 
       "name": "Middelie, Middelie, Brink", 
       "id": "37501140"
     }, 
     {
       "lat": "4.8459341874984", 
       "lon": "52.5019482460193", 
       "name": "Wormer, Wormer, Keerlus Wormer - Oost", 
       "id": "37520010"
     }, 
     {
       "lat": "4.91969469795681", 
       "lon": "52.5083732630743", 
       "name": "Neck, Neck, Neckerbrug", 
       "id": "37520020"
     }, 
     {
       "lat": "4.84753746825065", 
       "lon": "52.5057302937624", 
       "name": "Jisp, Jisp, 't Weiver", 
       "id": "37520030"
     }, 
     {
       "lat": "4.90323906130383", 
       "lon": "52.5099699683459", 
       "name": "Jisp, Jisp, Laan", 
       "id": "37520040"
     }, 
     {
       "lat": "4.84849990984733", 
       "lon": "52.5077298878641", 
       "name": "Jisp, Jisp, De Lepelaar", 
       "id": "37520050"
     }, 
     {
       "lat": "4.88337668085364", 
       "lon": "52.5066428291242", 
       "name": "Jisp, Jisp, Goos", 
       "id": "37520060"
     }, 
     {
       "lat": "4.85192074686405", 
       "lon": "52.5074308072003", 
       "name": "Jisp, Jisp, De Bonte Os", 
       "id": "37520070"
     }, 
     {
       "lat": "4.86632128496361", 
       "lon": "52.5065781736222", 
       "name": "Jisp, Jisp, Boerderij Muis", 
       "id": "37520080"
     }, 
     {
       "lat": "4.85700605947515", 
       "lon": "52.5071211020471", 
       "name": "Jisp, Jisp, Brandweerkazerne", 
       "id": "37520090"
     }, 
     {
       "lat": "4.85693090747894", 
       "lon": "52.5072465908616", 
       "name": "Jisp, Jisp, Brandweerkazerne", 
       "id": "37520100"
     }, 
     {
       "lat": "4.86641113731853", 
       "lon": "52.5064527434472", 
       "name": "Jisp, Jisp, Boerderij Muis", 
       "id": "37520110"
     }, 
     {
       "lat": "4.85211080180493", 
       "lon": "52.5075485016012", 
       "name": "Jisp, Jisp, De Bonte Os", 
       "id": "37520120"
     }, 
     {
       "lat": "4.88351056713734", 
       "lon": "52.5065265605628", 
       "name": "Jisp, Jisp, Goos", 
       "id": "37520130"
     }, 
     {
       "lat": "4.84852794241095", 
       "lon": "52.5078468523437", 
       "name": "Jisp, Jisp, De Lepelaar", 
       "id": "37520140"
     }, 
     {
       "lat": "4.90318162067686", 
       "lon": "52.5098349224654", 
       "name": "Jisp, Jisp, Laan", 
       "id": "37520150"
     }, 
     {
       "lat": "4.8477434391812", 
       "lon": "52.5057492053431", 
       "name": "Jisp, Jisp, 't Weiver", 
       "id": "37520160"
     }, 
     {
       "lat": "5.01701234376438", 
       "lon": "52.6296223493275", 
       "name": "Scharwoude, Scharwoude, Gemaal Westerkogge", 
       "id": "38000020"
     }, 
     {
       "lat": "5.05352652175264", 
       "lon": "52.6448467176137", 
       "name": "Hoorn, Hoorn, Station", 
       "id": "38000234"
     }, 
     {
       "lat": "5.03137377618385", 
       "lon": "52.6381410421902", 
       "name": "Hoorn, Hoorn, Houtzaagmolen", 
       "id": "38001510"
     }, 
     {
       "lat": "5.02496333152511", 
       "lon": "52.638022831456", 
       "name": "Hoorn, Hoorn, Korenmolen", 
       "id": "38001530"
     }, 
     {
       "lat": "5.02629690451251", 
       "lon": "52.6375325948135", 
       "name": "Hoorn, Hoorn, Korenmolen", 
       "id": "38001540"
     }, 
     {
       "lat": "5.02064099456349", 
       "lon": "52.637290618547", 
       "name": "Hoorn, Hoorn, Verfmolen", 
       "id": "38001550"
     }, 
     {
       "lat": "5.02174361119084", 
       "lon": "52.6379320969838", 
       "name": "Hoorn, Hoorn, Verfmolen", 
       "id": "38001560"
     }, 
     {
       "lat": "5.02187827513502", 
       "lon": "52.6359463585537", 
       "name": "Hoorn, Hoorn, Poldermolen", 
       "id": "38001570"
     }, 
     {
       "lat": "5.02199592713202", 
       "lon": "52.6360096297257", 
       "name": "Hoorn, Hoorn, Poldermolen", 
       "id": "38001580"
     }, 
     {
       "lat": "5.03141882009332", 
       "lon": "52.6380513058781", 
       "name": "Hoorn, Hoorn, Houtzaagmolen", 
       "id": "38001610"
     }, 
     {
       "lat": "5.04061384054433", 
       "lon": "52.6691377692097", 
       "name": "Hoorn, Hoorn, Kromme Elleboog", 
       "id": "38002010"
     }, 
     {
       "lat": "5.0412775874057", 
       "lon": "52.6693284284073", 
       "name": "Hoorn, Hoorn, Kromme Elleboog", 
       "id": "38002020"
     }, 
     {
       "lat": "5.0221014911945", 
       "lon": "52.6357493274923", 
       "name": "t.h.v. Bussluis Grote Waal, t.h.v. Bussluis Grote Waal", 
       "id": "38009629"
     }, 
     {
       "lat": "5.05376686742569", 
       "lon": "52.64432614075", 
       "name": "t.h.v. Station NS, t.h.v. Station NS", 
       "id": "38009639"
     }, 
     {
       "lat": "5.05358950413362", 
       "lon": "52.6443346305029", 
       "name": "t.h.v. Station NS, t.h.v. Station NS", 
       "id": "38009649"
     }, 
     {
       "lat": "5.02221921750433", 
       "lon": "52.6358036115588", 
       "name": "t.h.v. Bussluis Grote Waal, t.h.v. Bussluis Grote Waal", 
       "id": "38009659"
     }, 
     {
       "lat": "5.09571090828914", 
       "lon": "52.6490736470186", 
       "name": "Hoorn, Hoorn, Scheldeweg", 
       "id": "38113000"
     }, 
     {
       "lat": "5.09911275618484", 
       "lon": "52.6530901592417", 
       "name": "Hoorn, Hoorn, Glenn Millerhof", 
       "id": "38113250"
     }, 
     {
       "lat": "5.09730974657659", 
       "lon": "52.6553505152105", 
       "name": "Hoorn, Hoorn, Gerrit Achterberghof", 
       "id": "38113270"
     }, 
     {
       "lat": "5.01687692261546", 
       "lon": "52.6299185030055", 
       "name": "Scharwoude, Scharwoude, Gemaal Westerkogge", 
       "id": "38190010"
     }, 
     {
       "lat": "5.01255379507626", 
       "lon": "52.6224456334385", 
       "name": "Scharwoude, Scharwoude, Ooms", 
       "id": "38190030"
     }, 
     {
       "lat": "5.00365395953832", 
       "lon": "52.6015220718399", 
       "name": "Oudendijk, Oudendijk, N247", 
       "id": "38190040"
     }, 
     {
       "lat": "5.00705758028028", 
       "lon": "52.6210441657775", 
       "name": "Scharwoude, Scharwoude, Rijksweg", 
       "id": "38190050"
     }, 
     {
       "lat": "5.00728032165926", 
       "lon": "52.6209010832772", 
       "name": "Scharwoude, Scharwoude, Rijksweg", 
       "id": "38190060"
     }, 
     {
       "lat": "5.01312979219883", 
       "lon": "52.6224384598967", 
       "name": "Scharwoude, Scharwoude, Ooms", 
       "id": "38190080"
     }, 
     {
       "lat": "5.00106140814641", 
       "lon": "52.5908099089174", 
       "name": "Beets, Beets, N247", 
       "id": "38290010"
     }, 
     {
       "lat": "5.00832786088437", 
       "lon": "52.5626402994407", 
       "name": "Warder, Warder, Verkavelingweg", 
       "id": "38290020"
     }, 
     {
       "lat": "4.99890458035482", 
       "lon": "52.5743202812477", 
       "name": "Oosthuizen, Oosthuizen, Dorp", 
       "id": "38290040"
     }, 
     {
       "lat": "4.99785574795612", 
       "lon": "52.574487606461", 
       "name": "Oosthuizen, Oosthuizen, Dorp", 
       "id": "38290043"
     }, 
     {
       "lat": "4.99884779227027", 
       "lon": "52.5740684523892", 
       "name": "Oosthuizen, Oosthuizen, Dorp", 
       "id": "38290050"
     }, 
     {
       "lat": "4.9976783377228", 
       "lon": "52.5745319611966", 
       "name": "Oosthuizen, Oosthuizen, Dorp", 
       "id": "38290053"
     }, 
     {
       "lat": "4.99328288774455", 
       "lon": "52.5695205484988", 
       "name": "Oosthuizen, Oosthuizen, Seevancksweg", 
       "id": "38290060"
     }, 
     {
       "lat": "4.99315078516785", 
       "lon": "52.5694482121981", 
       "name": "Oosthuizen, Oosthuizen, Seevancksweg", 
       "id": "38290070"
     }, 
     {
       "lat": "4.99238360048414", 
       "lon": "52.5711172969886", 
       "name": "Oosthuizen, Oosthuizen, Kerk", 
       "id": "38290080"
     }, 
     {
       "lat": "4.99216210938387", 
       "lon": "52.5711435224504", 
       "name": "Oosthuizen, Oosthuizen, Kerk", 
       "id": "38290090"
     }, 
     {
       "lat": "4.99635814474347", 
       "lon": "52.5736918100867", 
       "name": "Oosthuizen, Oosthuizen, Bejaardenhuis", 
       "id": "38290100"
     }, 
     {
       "lat": "4.99619540738193", 
       "lon": "52.5737451981437", 
       "name": "Oosthuizen, Oosthuizen, Bejaardenhuis", 
       "id": "38290110"
     }, 
     {
       "lat": "5.02236447687644", 
       "lon": "52.5844064233665", 
       "name": "Etersheim, Etersheim, No 12", 
       "id": "38290130"
     }, 
     {
       "lat": "5.03185885021927", 
       "lon": "52.5652294586672", 
       "name": "Warder, Warder, IJsselmeerdijk", 
       "id": "38290150"
     }, 
     {
       "lat": "5.02991894947813", 
       "lon": "52.5643788370035", 
       "name": "Warder, Warder, N.H.Kerk", 
       "id": "38290170"
     }, 
     {
       "lat": "5.0211359578018", 
       "lon": "52.5671021983385", 
       "name": "Warder, Warder, Boerderij Beunder", 
       "id": "38290190"
     }, 
     {
       "lat": "5.01409795774503", 
       "lon": "52.5691653466832", 
       "name": "Warder, Warder, Westerweg", 
       "id": "38290210"
     }, 
     {
       "lat": "5.00613920684946", 
       "lon": "52.5718722111811", 
       "name": "Warder, Warder, Noodslachtplaats", 
       "id": "38290230"
     }, 
     {
       "lat": "5.00140243170575", 
       "lon": "52.57545182607", 
       "name": "Oosthuizen, Oosthuizen, Warderweg", 
       "id": "38290250"
     }, 
     {
       "lat": "5.00115061388981", 
       "lon": "52.5924189112488", 
       "name": "Beets, Beets, N247", 
       "id": "38290320"
     }, 
     {
       "lat": "5.00113680144728", 
       "lon": "52.5923110197481", 
       "name": "Beets, Beets, N247", 
       "id": "38290330"
     }, 
     {
       "lat": "5.01771653068492", 
       "lon": "52.5967494824204", 
       "name": "Schardam, Schardam, Camping Schardam", 
       "id": "38291020"
     }, 
     {
       "lat": "5.01348111588919", 
       "lon": "52.6019218529852", 
       "name": "Schardam, Schardam, Laag Schardammerweg", 
       "id": "38291040"
     }, 
     {
       "lat": "5.00358305374303", 
       "lon": "52.6011893166457", 
       "name": "Oudendijk, Oudendijk, N247", 
       "id": "38291060"
     }, 
     {
       "lat": "5.00234933033672", 
       "lon": "52.5700625413504", 
       "name": "t.h.v. Spoorwegovergang, t.h.v. Spoorwegovergang", 
       "id": "38299619"
     }, 
     {
       "lat": "5.00197949050029", 
       "lon": "52.5701871643309", 
       "name": "t.h.v. Spoorwegovergang, t.h.v. Spoorwegovergang", 
       "id": "38299629"
     }, 
     {
       "lat": "4.97651829607451", 
       "lon": "52.5482807040899", 
       "name": "Hobrede, Hobrede, Brug", 
       "id": "38381010"
     }, 
     {
       "lat": "4.97639742944115", 
       "lon": "52.5485948423138", 
       "name": "Hobrede, Hobrede, Brug", 
       "id": "38381020"
     }, 
     {
       "lat": "5.00910580546925", 
       "lon": "52.5613486101131", 
       "name": "Warder, Warder, Verkavelingweg", 
       "id": "38390010"
     }, 
     {
       "lat": "5.04580970062846", 
       "lon": "52.5158222064285", 
       "name": "Edam, Edam, Technische School", 
       "id": "38390020"
     }, 
     {
       "lat": "5.02621637616872", 
       "lon": "52.541045623383", 
       "name": "Middelie, Middelie, Klemweg (N247)", 
       "id": "38390030"
     }, 
     {
       "lat": "5.03667912880857", 
       "lon": "52.5284138316699", 
       "name": "Zeevang, Zeevang, Riethoorneweg", 
       "id": "38390040"
     }, 
     {
       "lat": "5.03845255793165", 
       "lon": "52.5259025999451", 
       "name": "Zeevang, Zeevang, Riethoorneweg", 
       "id": "38390050"
     }, 
     {
       "lat": "5.02578200025764", 
       "lon": "52.541889109566", 
       "name": "Middelie, Middelie, Klemweg (N247)", 
       "id": "38390060"
     }, 
     {
       "lat": "4.99948066183289", 
       "lon": "52.5524201597553", 
       "name": "Middelie, Middelie, Spoorwegovergang", 
       "id": "38391010"
     }, 
     {
       "lat": "4.99962754657292", 
       "lon": "52.5524835503308", 
       "name": "Middelie, Middelie, Spoorwegovergang", 
       "id": "38391020"
     }, 
     {
       "lat": "5.00434865499508", 
       "lon": "52.5487421704584", 
       "name": "Middelie, Middelie, Vroom B.V.", 
       "id": "38391030"
     }, 
     {
       "lat": "5.00448071404287", 
       "lon": "52.5488144946046", 
       "name": "Middelie, Middelie, Vroom B.V.", 
       "id": "38391040"
     }, 
     {
       "lat": "5.04444051588593", 
       "lon": "52.5100124232692", 
       "name": "Edam, Edam, Busstation", 
       "id": "38490011"
     }, 
     {
       "lat": "5.04445426947705", 
       "lon": "52.5101382861665", 
       "name": "Edam, Edam, Busstation", 
       "id": "38490012"
     }, 
     {
       "lat": "5.04445426947705", 
       "lon": "52.5101382861665", 
       "name": "Edam, Edam, Busstation", 
       "id": "38490013"
     }, 
     {
       "lat": "5.0444685808629", 
       "lon": "52.510192251713", 
       "name": "Edam, Edam, Busstation", 
       "id": "38490014"
     }, 
     {
       "lat": "5.04449755228323", 
       "lon": "52.5102552469583", 
       "name": "Edam, Edam, Busstation", 
       "id": "38490015"
     }, 
     {
       "lat": "5.04454118381848", 
       "lon": "52.5103272718913", 
       "name": "Edam, Edam, Busstation", 
       "id": "38490016"
     }, 
     {
       "lat": "5.04457043420728", 
       "lon": "52.5103543184451", 
       "name": "Edam, Edam, Busstation", 
       "id": "38490017"
     }, 
     {
       "lat": "5.03531532103387", 
       "lon": "52.4887395168738", 
       "name": "Katwoude, Katwoude, Hotel Volendam", 
       "id": "38490020"
     }, 
     {
       "lat": "5.04994612631562", 
       "lon": "52.5085273049968", 
       "name": "Edam, Edam, De Meermin", 
       "id": "38490030"
     }, 
     {
       "lat": "5.05709036399892", 
       "lon": "52.4926936465011", 
       "name": "Volendam, Volendam, Zeddeweg", 
       "id": "38490040"
     }, 
     {
       "lat": "5.05758137408161", 
       "lon": "52.4959574362867", 
       "name": "Volendam, Volendam, Dirk Visstraat", 
       "id": "38490060"
     }, 
     {
       "lat": "5.05747192473686", 
       "lon": "52.5027336212874", 
       "name": "Volendam, Volendam, Politiebureau", 
       "id": "38490070"
     }, 
     {
       "lat": "5.06192054314591", 
       "lon": "52.496607515159", 
       "name": "Volendam, Volendam, Junoplantsoen", 
       "id": "38490080"
     }, 
     {
       "lat": "5.06586120894295", 
       "lon": "52.497400154663", 
       "name": "Volendam, Volendam, Weegschaalstraat", 
       "id": "38490100"
     }, 
     {
       "lat": "5.07129764759352", 
       "lon": "52.4949701825105", 
       "name": "Volendam, Volendam, Zeestraat", 
       "id": "38490120"
     }, 
     {
       "lat": "5.07129764759352", 
       "lon": "52.4949701825105", 
       "name": "Volendam, Volendam, Zeestraat", 
       "id": "38490121"
     }, 
     {
       "lat": "5.07286150201504", 
       "lon": "52.5028293065251", 
       "name": "Volendam, Volendam, Mgr. C. Veermanlaan", 
       "id": "38490130"
     }, 
     {
       "lat": "5.07524679248947", 
       "lon": "52.4987373568871", 
       "name": "Volendam, Volendam, Vissersstraat", 
       "id": "38490140"
     }, 
     {
       "lat": "5.07492414551803", 
       "lon": "52.5027179161004", 
       "name": "Volendam, Volendam, Edisonstraat", 
       "id": "38490150"
     }, 
     {
       "lat": "5.07571992294076", 
       "lon": "52.5026481084041", 
       "name": "Volendam, Volendam, Edisonstraat", 
       "id": "38490180"
     }, 
     {
       "lat": "5.07242184066813", 
       "lon": "52.4942541788734", 
       "name": "Volendam, Volendam, Zeestraat (uitstap)", 
       "id": "38490190"
     }, 
     {
       "lat": "5.07243396315654", 
       "lon": "52.5028910849392", 
       "name": "Volendam, Volendam, Mgr. C. Veermanlaan", 
       "id": "38490200"
     }, 
     {
       "lat": "5.06594910441977", 
       "lon": "52.4974633043544", 
       "name": "Volendam, Volendam, Weegschaalstraat", 
       "id": "38490210"
     }, 
     {
       "lat": "5.06274330626206", 
       "lon": "52.4968614145839", 
       "name": "Volendam, Volendam, Junoplantsoen", 
       "id": "38490230"
     }, 
     {
       "lat": "5.05672699047067", 
       "lon": "52.4959999968305", 
       "name": "Volendam, Volendam, Dirk Visstraat", 
       "id": "38490250"
     }, 
     {
       "lat": "5.05755881326063", 
       "lon": "52.5029315850115", 
       "name": "Volendam, Volendam, Politiebureau", 
       "id": "38490260"
     }, 
     {
       "lat": "5.05708013672206", 
       "lon": "52.4920914622445", 
       "name": "Volendam, Volendam, Zeddeweg", 
       "id": "38490270"
     }, 
     {
       "lat": "5.05304483928861", 
       "lon": "52.5058488457025", 
       "name": "Edam, Edam, IJe", 
       "id": "38490280"
     }, 
     {
       "lat": "5.07502571345351", 
       "lon": "52.4987637376549", 
       "name": "Volendam, Volendam, Vissersstraat", 
       "id": "38490290"
     }, 
     {
       "lat": "5.04973785916549", 
       "lon": "52.5087963341081", 
       "name": "Edam, Edam, De Meermin", 
       "id": "38490300"
     }, 
     {
       "lat": "5.05837042779655", 
       "lon": "52.512613232921", 
       "name": "Edam, Edam, Keetzijde", 
       "id": "38490310"
     }, 
     {
       "lat": "5.04878060115249", 
       "lon": "52.4953125321888", 
       "name": "Volendam, Volendam, Leendert Spaanderlaan", 
       "id": "38490320"
     }, 
     {
       "lat": "5.05720615044618", 
       "lon": "52.5107136683603", 
       "name": "Edam, Edam, Broekgouwstraat", 
       "id": "38490330"
     }, 
     {
       "lat": "5.05720615044618", 
       "lon": "52.5107136683603", 
       "name": "Edam, Edam, Broekgouwstraat", 
       "id": "38490331"
     }, 
     {
       "lat": "5.04758529078395", 
       "lon": "52.4975649533979", 
       "name": "Volendam, Volendam, Schoener", 
       "id": "38490340"
     }, 
     {
       "lat": "5.05768616847522", 
       "lon": "52.5075784111439", 
       "name": "Edam, Edam, Weerenstraat", 
       "id": "38490350"
     }, 
     {
       "lat": "5.05079690262179", 
       "lon": "52.4993176554798", 
       "name": "Volendam, Volendam, Jan Platstraat", 
       "id": "38490360"
     }, 
     {
       "lat": "5.05410356417048", 
       "lon": "52.5002167346916", 
       "name": "Volendam, Volendam, Stadskantoor", 
       "id": "38490380"
     }, 
     {
       "lat": "5.05373547259068", 
       "lon": "52.5002067135107", 
       "name": "Volendam, Volendam, Stadskantoor", 
       "id": "38490390"
     }, 
     {
       "lat": "5.05229185938246", 
       "lon": "52.5060893823098", 
       "name": "Edam, Edam, IJe", 
       "id": "38490400"
     }, 
     {
       "lat": "5.05075204026577", 
       "lon": "52.4994074021784", 
       "name": "Volendam, Volendam, Jan Platstraat", 
       "id": "38490410"
     }, 
     {
       "lat": "5.05805398768724", 
       "lon": "52.5076333560178", 
       "name": "Edam, Edam, Weerenstraat", 
       "id": "38490420"
     }, 
     {
       "lat": "5.04721293673439", 
       "lon": "52.4981121181007", 
       "name": "Volendam, Volendam, Schoener", 
       "id": "38490430"
     }, 
     {
       "lat": "5.05727959852061", 
       "lon": "52.5107408346388", 
       "name": "Edam, Edam, Broekgouwstraat", 
       "id": "38490440"
     }, 
     {
       "lat": "5.05727959852061", 
       "lon": "52.5107408346388", 
       "name": "Edam, Edam, Broekgouwstraat", 
       "id": "38490441"
     }, 
     {
       "lat": "5.04897250408213", 
       "lon": "52.4952501675729", 
       "name": "Volendam, Volendam, Leendert Spaanderlaan", 
       "id": "38490450"
     }, 
     {
       "lat": "5.06602775508722", 
       "lon": "52.5089314077699", 
       "name": "Edam, Edam, Tjaskermolen", 
       "id": "38490480"
     }, 
     {
       "lat": "5.0608183659413", 
       "lon": "52.5082701060874", 
       "name": "Edam, Edam, Watermolen", 
       "id": "38490500"
     }, 
     {
       "lat": "5.06458495013606", 
       "lon": "52.4926962858041", 
       "name": "Volendam, Volendam, Prinses Margrietstraat", 
       "id": "38490510"
     }, 
     {
       "lat": "5.05309087399806", 
       "lon": "52.4958639908159", 
       "name": "Volendam, Volendam, Kraggenburg", 
       "id": "38490520"
     }, 
     {
       "lat": "5.06182305313602", 
       "lon": "52.5078504584829", 
       "name": "Edam, Edam, Watermolen", 
       "id": "38490530"
     }, 
     {
       "lat": "5.06463036775976", 
       "lon": "52.4925256487467", 
       "name": "Volendam, Volendam, Prinses Margrietstraat", 
       "id": "38490540"
     }, 
     {
       "lat": "5.06627789202735", 
       "lon": "52.5089680338457", 
       "name": "Edam, Edam, Tjaskermolen", 
       "id": "38490550"
     }, 
     {
       "lat": "5.05621686546082", 
       "lon": "52.4952975582866", 
       "name": "Volendam, Volendam, Heideweg", 
       "id": "38490560"
     }, 
     {
       "lat": "5.05837042779655", 
       "lon": "52.512613232921", 
       "name": "Edam, Edam, Keetzijde", 
       "id": "38490580"
     }, 
     {
       "lat": "5.06976157309387", 
       "lon": "52.4956221625941", 
       "name": "Volendam, Volendam, Populierenlaan", 
       "id": "38490590"
     }, 
     {
       "lat": "5.06987655572732", 
       "lon": "52.5083216323992", 
       "name": "Volendam, Volendam, G.A. Brederodestraat", 
       "id": "38490610"
     }, 
     {
       "lat": "5.07094091021695", 
       "lon": "52.5077852315229", 
       "name": "Volendam, Volendam, G.A. Brederodestraat", 
       "id": "38490620"
     }, 
     {
       "lat": "5.07102726860642", 
       "lon": "52.4957154156575", 
       "name": "Volendam, Volendam, Julianaweg / Centrum", 
       "id": "38490630"
     }, 
     {
       "lat": "5.0703702525159", 
       "lon": "52.494931760382", 
       "name": "Volendam, Volendam, Julianaweg / Centrum", 
       "id": "38490640"
     }, 
     {
       "lat": "5.04444051588593", 
       "lon": "52.5100124232692", 
       "name": "Edam, Edam, Busstation", 
       "id": "38491011"
     }, 
     {
       "lat": "5.04445426947705", 
       "lon": "52.5101382861665", 
       "name": "Edam, Edam, Busstation", 
       "id": "38491012"
     }, 
     {
       "lat": "5.04454118381848", 
       "lon": "52.5103272718913", 
       "name": "Edam, Edam, Busstation", 
       "id": "38491016"
     }, 
     {
       "lat": "5.04457043420728", 
       "lon": "52.5103543184451", 
       "name": "Edam, Edam, Busstation", 
       "id": "38491017"
     }, 
     {
       "lat": "5.04544467916936", 
       "lon": "52.5153987501594", 
       "name": "Edam, Edam, Technische School", 
       "id": "38491510"
     }, 
     {
       "lat": "5.05983586944905", 
       "lon": "52.5017156046164", 
       "name": "t.h.v. Politiebureau, t.h.v. Politiebureau", 
       "id": "38499610"
     }, 
     {
       "lat": "5.07278835610043", 
       "lon": "52.5069003909635", 
       "name": "t.h.v. Kruising Harlingenlaan, t.h.v. Kruising Harlingenlaan", 
       "id": "38499629"
     }, 
     {
       "lat": "5.0727280345294", 
       "lon": "52.5070979531736", 
       "name": "t.h.v. Kruising Harlingenlaan, t.h.v. Kruising Harlingenlaan", 
       "id": "38499639"
     }, 
     {
       "lat": "5.03736908742087", 
       "lon": "52.5045634137256", 
       "name": "t.h.v. Kruising N244/N247, t.h.v. Kruising N244/N247", 
       "id": "38499649"
     }, 
     {
       "lat": "5.04277876479267", 
       "lon": "52.5058824074694", 
       "name": "t.h.v. Kruising N244/N247, t.h.v. Kruising N244/N247", 
       "id": "38499659"
     }, 
     {
       "lat": "5.03537421114445", 
       "lon": "52.488739691523", 
       "name": "t.h.v. Hotel Volendam, t.h.v. Hotel Volendam", 
       "id": "38499669"
     }, 
     {
       "lat": "5.03450479340139", 
       "lon": "52.4888359717176", 
       "name": "t.h.v. Hotel Volendam, t.h.v. Hotel Volendam", 
       "id": "38499679"
     }, 
     {
       "lat": "5.05647948439417", 
       "lon": "52.5034947868852", 
       "name": "t.h.v. Politiebureau, t.h.v. Politiebureau", 
       "id": "38499699"
     }, 
     {
       "lat": "5.05794634274236", 
       "lon": "52.502312531654", 
       "name": "t.h.v. Politiebureau, t.h.v. Politiebureau", 
       "id": "38499709"
     }, 
     {
       "lat": "5.03901662003859", 
       "lon": "52.5029505297207", 
       "name": "t.h.v. Kruising N244/N247, t.h.v. Kruising N244/N247", 
       "id": "38499719"
     }, 
     {
       "lat": "4.90578165637893", 
       "lon": "52.3739084850559", 
       "name": "Amsterdam, Amsterdam, Pr. Hendrikkade", 
       "id": "57003040"
     }, 
     {
       "lat": "4.91198344301755", 
       "lon": "52.3720910594694", 
       "name": "t.h.v. IJtunnel, t.h.v. IJtunnel", 
       "id": "57009616"
     }, 
     {
       "lat": "4.91114377730275", 
       "lon": "52.3723393421056", 
       "name": "t.h.v. IJtunnel, t.h.v. IJtunnel", 
       "id": "57009629"
     }, 
     {
       "lat": "4.91519753550344", 
       "lon": "52.4067513651101", 
       "name": "Amsterdam, Amsterdam, Koopvaardersplantsoen", 
       "id": "57111184"
     }, 
     {
       "lat": "4.91611417275087", 
       "lon": "52.4062337308061", 
       "name": "Amsterdam, Amsterdam, Koopvaardersplantsoen", 
       "id": "57111185"
     }, 
     {
       "lat": "4.91386144133651", 
       "lon": "52.4080132906749", 
       "name": "Amsterdam, Amsterdam, Statenjachtstraat", 
       "id": "57111277"
     }, 
     {
       "lat": "4.91361286643416", 
       "lon": "52.4078954580698", 
       "name": "Amsterdam, Amsterdam, Statenjachtstraat", 
       "id": "57111278"
     }, 
     {
       "lat": "4.92817399778823", 
       "lon": "52.4038993495518", 
       "name": "Amsterdam, Amsterdam, G.J.Scheurleerweg", 
       "id": "57111339"
     }, 
     {
       "lat": "4.9297541592047", 
       "lon": "52.40314151301", 
       "name": "Amsterdam, Amsterdam, G.J.Scheurleerweg", 
       "id": "57111340"
     }, 
     {
       "lat": "4.92242037158264", 
       "lon": "52.4060609109124", 
       "name": "Amsterdam, Amsterdam, Oosterlengte", 
       "id": "57111351"
     }, 
     {
       "lat": "4.92227653446646", 
       "lon": "52.4057637547143", 
       "name": "Amsterdam, Amsterdam, Oosterlengte", 
       "id": "57111352"
     }, 
     {
       "lat": "4.90982620362434", 
       "lon": "52.4238063220077", 
       "name": "Landsmeer, Landsmeer, Zuideinde 90", 
       "id": "57112390"
     }, 
     {
       "lat": "4.90819697405578", 
       "lon": "52.4194856952533", 
       "name": "Amsterdam, Amsterdam, Vorticellaweg", 
       "id": "57112410"
     }, 
     {
       "lat": "4.90801892962204", 
       "lon": "52.419637764822", 
       "name": "Amsterdam, Amsterdam, Vorticellaweg", 
       "id": "57112800"
     }, 
     {
       "lat": "4.93466163356394", 
       "lon": "52.4003112817723", 
       "name": "Amsterdam, Amsterdam, Buikslotermeerplein", 
       "id": "57114030"
     }, 
     {
       "lat": "4.92843183087115", 
       "lon": "52.3946071287566", 
       "name": "Amsterdam, Amsterdam, Rode Kruisstraat", 
       "id": "57114050"
     }, 
     {
       "lat": "4.91194755334143", 
       "lon": "52.3905156637328", 
       "name": "Amsterdam, Amsterdam, Gentiaanstraat", 
       "id": "57114080"
     }, 
     {
       "lat": "4.92489222065828", 
       "lon": "52.3888682299367", 
       "name": "Amsterdam, Amsterdam, Merelstraat", 
       "id": "57114090"
     }, 
     {
       "lat": "4.9134722162546", 
       "lon": "52.3880591511018", 
       "name": "Amsterdam, Amsterdam, Hagedoornplein", 
       "id": "57114100"
     }, 
     {
       "lat": "4.92100007442419", 
       "lon": "52.3860128711766", 
       "name": "Amsterdam, Amsterdam, Hamerstraat", 
       "id": "57114110"
     }, 
     {
       "lat": "4.91502273624581", 
       "lon": "52.3859172896934", 
       "name": "Amsterdam, Amsterdam, Kraaienplein", 
       "id": "57114120"
     }, 
     {
       "lat": "4.91764637026855", 
       "lon": "52.385064904346", 
       "name": "Amsterdam, Amsterdam, Havikslaan", 
       "id": "57114130"
     }, 
     {
       "lat": "4.91827547905597", 
       "lon": "52.385301076416", 
       "name": "Amsterdam, Amsterdam, Havikslaan", 
       "id": "57114140"
     }, 
     {
       "lat": "4.91494671083171", 
       "lon": "52.3861596537001", 
       "name": "Amsterdam, Amsterdam, Kraaienplein", 
       "id": "57114150"
     }, 
     {
       "lat": "4.92271661993999", 
       "lon": "52.3862083567576", 
       "name": "Amsterdam, Amsterdam, Hamerstraat", 
       "id": "57114160"
     }, 
     {
       "lat": "4.9136637477589", 
       "lon": "52.3880059910329", 
       "name": "Amsterdam, Amsterdam, Hagedoornplein", 
       "id": "57114170"
     }, 
     {
       "lat": "4.92515409702378", 
       "lon": "52.3891119186774", 
       "name": "Amsterdam, Amsterdam, Merelstraat", 
       "id": "57114180"
     }, 
     {
       "lat": "4.91168101797847", 
       "lon": "52.3907123225723", 
       "name": "Amsterdam, Amsterdam, Gentiaanstraat", 
       "id": "57114190"
     }, 
     {
       "lat": "4.92884113686082", 
       "lon": "52.3948064415862", 
       "name": "Amsterdam, Amsterdam, Rode Kruisstraat", 
       "id": "57114200"
     }, 
     {
       "lat": "4.93520454090412", 
       "lon": "52.4003852555782", 
       "name": "Amsterdam, Amsterdam, Buikslotermeerplein", 
       "id": "57114220"
     }, 
     {
       "lat": "4.90417434458935", 
       "lon": "52.382611012935", 
       "name": "Amsterdam, Amsterdam, Buiksloterweg [Veer]", 
       "id": "57114270"
     }, 
     {
       "lat": "4.90417434458935", 
       "lon": "52.382611012935", 
       "name": "Amsterdam, Amsterdam, Buiksloterweg [Veer]", 
       "id": "57114271"
     }, 
     {
       "lat": "4.91137308240638", 
       "lon": "52.4139261693375", 
       "name": "Amsterdam, Amsterdam, Kadoelenpad", 
       "id": "57115010"
     }, 
     {
       "lat": "4.91148233390189", 
       "lon": "52.4133334249507", 
       "name": "Amsterdam, Amsterdam, Kadoelenpad", 
       "id": "57115020"
     }, 
     {
       "lat": "4.92010189767528", 
       "lon": "52.4057372253816", 
       "name": "Amsterdam, Amsterdam, Boven IJ Ziekenhuis", 
       "id": "57115050"
     }, 
     {
       "lat": "4.92004719257095", 
       "lon": "52.4053505414728", 
       "name": "Amsterdam, Amsterdam, Boven IJ Ziekenhuis", 
       "id": "57115060"
     }, 
     {
       "lat": "4.91144952704982", 
       "lon": "52.4027009234135", 
       "name": "Amsterdam, Amsterdam, Barkpad", 
       "id": "57115090"
     }, 
     {
       "lat": "4.91175944543823", 
       "lon": "52.4025763406409", 
       "name": "Amsterdam, Amsterdam, Barkpad", 
       "id": "57115100"
     }, 
     {
       "lat": "4.92482651442868", 
       "lon": "52.4050277610319", 
       "name": "t.h.v. brug Noord Hollandsch Kanaal, t.h.v. brug Noord Hollandsch Kanaal", 
       "id": "57119619"
     }, 
     {
       "lat": "4.92469510779488", 
       "lon": "52.4049463594122", 
       "name": "t.h.v. brug Noord Hollandsch Kanaal, t.h.v. brug Noord Hollandsch Kanaal", 
       "id": "57119629"
     }, 
     {
       "lat": "4.9134457194473", 
       "lon": "52.387789415042", 
       "name": "t.h.v. Hagedoornplein, t.h.v. Hagedoornplein", 
       "id": "57119639"
     }, 
     {
       "lat": "4.91349900144655", 
       "lon": "52.3883019252882", 
       "name": "t.h.v. Hagedoornplein, t.h.v. Hagedoornplein", 
       "id": "57119649"
     }, 
     {
       "lat": "4.9079618993143", 
       "lon": "52.4208328865882", 
       "name": "t.h.v. Kruising A10 Noord, t.h.v. Kruising A10 Noord", 
       "id": "57119659"
     }, 
     {
       "lat": "4.90727948278274", 
       "lon": "52.4200482024907", 
       "name": "t.h.v. Kruising A10 Noord, t.h.v. Kruising A10 Noord", 
       "id": "57119669"
     }, 
     {
       "lat": "4.84997667151176", 
       "lon": "52.3704777947063", 
       "name": "Amsterdam, Amsterdam, Mercatorplein", 
       "id": "57134000"
     }, 
     {
       "lat": "4.84047364993294", 
       "lon": "52.3587771738272", 
       "name": "Amsterdam, Amsterdam, J.Jongkindstraat", 
       "id": "57134010"
     }, 
     {
       "lat": "4.83902070963311", 
       "lon": "52.3563707197854", 
       "name": "Amsterdam, Amsterdam, Kon. Wilhelminaplein", 
       "id": "57134030"
     }, 
     {
       "lat": "4.8400197178838", 
       "lon": "52.3563034398662", 
       "name": "Amsterdam, Amsterdam, Kon. Wilhelminaplein", 
       "id": "57134120"
     }, 
     {
       "lat": "4.84073521663971", 
       "lon": "52.3589940880055", 
       "name": "Amsterdam, Amsterdam, J.Jongkindstraat", 
       "id": "57134140"
     }, 
     {
       "lat": "4.85010762104521", 
       "lon": "52.370577253943", 
       "name": "Amsterdam, Amsterdam, Mercatorplein", 
       "id": "57134160"
     }, 
     {
       "lat": "4.84041905189427", 
       "lon": "52.3632078887163", 
       "name": "Amsterdam, Amsterdam, M.Bauerstraat", 
       "id": "57134170"
     }, 
     {
       "lat": "4.84056231376569", 
       "lon": "52.3634961585898", 
       "name": "Amsterdam, Amsterdam, M.Bauerstraat", 
       "id": "57134180"
     }, 
     {
       "lat": "4.84367622264585", 
       "lon": "52.369370509674", 
       "name": "Amsterdam, Amsterdam, Adm. Helfrichstraat", 
       "id": "57134230"
     }, 
     {
       "lat": "4.84432324568629", 
       "lon": "52.36929258853", 
       "name": "Amsterdam, Amsterdam, Adm. Helfrichstraat", 
       "id": "57134240"
     }, 
     {
       "lat": "4.83800541624938", 
       "lon": "52.3696139729416", 
       "name": "Amsterdam, Amsterdam, Jan Voermanstraat", 
       "id": "57134250"
     }, 
     {
       "lat": "4.83796225855369", 
       "lon": "52.3695418707487", 
       "name": "Amsterdam, Amsterdam, Jan Voermanstraat", 
       "id": "57134260"
     }, 
     {
       "lat": "4.8400784308377", 
       "lon": "52.3563037112596", 
       "name": "t.h.v. Koningin Wilhelminaplein, t.h.v. Koningin Wilhelminaplein", 
       "id": "57139619"
     }, 
     {
       "lat": "4.83573266931168", 
       "lon": "52.3563644347551", 
       "name": "t.h.v. Koningin Wilhelminaplein, t.h.v. Koningin Wilhelminaplein", 
       "id": "57139629"
     }, 
     {
       "lat": "4.97351965580877", 
       "lon": "52.328560899343", 
       "name": "Diemen, Diemen, Provincialeweg", 
       "id": "57250020"
     }, 
     {
       "lat": "4.97343071905936", 
       "lon": "52.3286594535727", 
       "name": "Diemen, Diemen, Provincialeweg", 
       "id": "57250030"
     }, 
     {
       "lat": "4.9549870329094", 
       "lon": "52.3230121249267", 
       "name": "Amsterdam-ZO, Amsterdam-ZO, Develstein", 
       "id": "57250180"
     }, 
     {
       "lat": "4.95396206536222", 
       "lon": "52.3228286210041", 
       "name": "Amsterdam-ZO, Amsterdam-ZO, Develstein", 
       "id": "57250250"
     }, 
     {
       "lat": "4.94638360686845", 
       "lon": "52.3105143346526", 
       "name": "Amsterdam-ZO, Amsterdam-ZO, Hoogoorddreef/Atlas", 
       "id": "57252100"
     }, 
     {
       "lat": "4.94694107931878", 
       "lon": "52.3104894473813", 
       "name": "Amsterdam-ZO, Amsterdam-ZO, Hoogoorddreef/Atlas", 
       "id": "57252830"
     }, 
     {
       "lat": "4.95970240317218", 
       "lon": "52.2978994157077", 
       "name": "Amsterdam-ZO, Amsterdam-ZO, Holendrechtstation", 
       "id": "57252940"
     }, 
     {
       "lat": "4.96533599840803", 
       "lon": "52.3267973705383", 
       "name": "Amsterdam-ZO, Amsterdam-ZO, Egeldonk/Daalwijkdreef", 
       "id": "57252960"
     }, 
     {
       "lat": "4.94463030764774", 
       "lon": "52.3069306461607", 
       "name": "Amsterdam-ZO, Amsterdam-ZO, Hondsrugweg/Atlas", 
       "id": "57253140"
     }, 
     {
       "lat": "4.94964712563272", 
       "lon": "52.3126655441201", 
       "name": "Amsterdam-ZO, Amsterdam-ZO,Foppingadreef", 
       "id": "57253660"
     }, 
     {
       "lat": "4.94982212072097", 
       "lon": "52.3127650568779", 
       "name": "t.h.v. Bijlmerstation, t.h.v. Bijlmerstation", 
       "id": "57259619"
     }, 
     {
       "lat": "4.94976576481863", 
       "lon": "52.3125311661154", 
       "name": "t.h.v. Bijlmerstation, t.h.v. Bijlmerstation", 
       "id": "57259629"
     }, 
     {
       "lat": "4.9324486607692", 
       "lon": "52.5800789966656", 
       "name": "Noordbeemster, Noordbeemster, Oosthuizerweg", 
       "id": "36371051"
     }, 
     {
       "lat": "4.9324486607692", 
       "lon": "52.5800789966656", 
       "name": "Noordbeemster, Noordbeemster, Oosthuizerweg", 
       "id": "36371061"
     }, 
     {
       "lat": "4.91096303241178", 
       "lon": "52.5449891671629", 
       "name": "Middenbeemster, Middenbeemster, K.Hogetoornlaan", 
       "id": "36470410"
     }, 
     {
       "lat": "4.92220289908912", 
       "lon": "52.5639430779997", 
       "name": "t.h.v. Hobredeweg, t.h.v. Hobredeweg", 
       "id": "36479940"
     }, 
     {
       "lat": "4.92240889005438", 
       "lon": "52.5639888208774", 
       "name": "t.h.v. Hobredeweg, t.h.v. Hobredeweg", 
       "id": "36479950"
     }, 
     {
       "lat": "4.90564483578342", 
       "lon": "52.5365555327571", 
       "name": "Zuidoostbeemster, Zuidoostbeemster, Kleine Bijenkorf", 
       "id": "36570030"
     }, 
     {
       "lat": "4.92417912418443", 
       "lon": "52.5175759910911", 
       "name": "Zuidoostbeemster, Zuidoostbeemster, Zuiderw./Nekkerw.", 
       "id": "36570050"
     }, 
     {
       "lat": "4.93151853867885", 
       "lon": "52.5158967893277", 
       "name": "Zuidoostbeemster, Zuidoostbeemster, Kolkpad", 
       "id": "36570070"
     }, 
     {
       "lat": "4.93113338728977", 
       "lon": "52.516102020381", 
       "name": "Zuidoostbeemster, Zuidoostbeemster, Kolkpad", 
       "id": "36570080"
     }, 
     {
       "lat": "4.93768926682534", 
       "lon": "52.5146441093701", 
       "name": "Zuidoostbeemster, Zuidoostbeemster, D.Dekkerstraat", 
       "id": "36570520"
     }, 
     {
       "lat": "4.92492101267979", 
       "lon": "52.5198886475438", 
       "name": "t.h.v. Zuiderpad, t.h.v. Zuiderpad", 
       "id": "36579930"
     }, 
     {
       "lat": "4.925097711644", 
       "lon": "52.5198983230458", 
       "name": "t.h.v. Zuiderpad, t.h.v. Zuiderpad", 
       "id": "36579940"
     }, 
     {
       "lat": "4.94908892837861", 
       "lon": "52.4495365693643", 
       "name": "Ilpendam, Ilpendam, Jaagweg", 
       "id": "37201060"
     }, 
     {
       "lat": "4.94764337483235", 
       "lon": "52.4780755400537", 
       "name": "Ilpendam, Ilpendam, Purmerlandersteiger", 
       "id": "37302020"
     }, 
     {
       "lat": "4.90960150904137", 
       "lon": "52.4500940863529", 
       "name": "Den Ilp, Den Ilp, Nr 68", 
       "id": "37312180"
     }, 
     {
       "lat": "4.90850526152137", 
       "lon": "52.4521657897142", 
       "name": "Den Ilp, Den Ilp, Nr 93", 
       "id": "37312200"
     }, 
     {
       "lat": "4.90760210021396", 
       "lon": "52.4540585125735", 
       "name": "Den Ilp, Den Ilp, Nr 107", 
       "id": "37312220"
     }, 
     {
       "lat": "4.90662833016814", 
       "lon": "52.4556723279334", 
       "name": "Den Ilp, Den Ilp, Nr 122", 
       "id": "37312240"
     }, 
     {
       "lat": "4.90550544907159", 
       "lon": "52.4588134112554", 
       "name": "Den Ilp, Den Ilp, Nr 141", 
       "id": "37312260"
     }, 
     {
       "lat": "4.90725659371549", 
       "lon": "52.4614987981857", 
       "name": "Den Ilp, Den Ilp, Molenzijl", 
       "id": "37312280"
     }, 
     {
       "lat": "4.90732733302609", 
       "lon": "52.4617597229527", 
       "name": "Den Ilp, Den Ilp, Molenzijl", 
       "id": "37312510"
     }, 
     {
       "lat": "4.9054047134142", 
       "lon": "52.4586062885494", 
       "name": "Den Ilp, Den Ilp, Nr 141", 
       "id": "37312530"
     }, 
     {
       "lat": "4.90648248621212", 
       "lon": "52.4555548986085", 
       "name": "Den Ilp, Den Ilp, Nr 122", 
       "id": "37312550"
     }, 
     {
       "lat": "4.90732142565139", 
       "lon": "52.4541652274413", 
       "name": "Den Ilp, Den Ilp, Nr 107", 
       "id": "37312570"
     }, 
     {
       "lat": "4.90843394703382", 
       "lon": "52.4519587880732", 
       "name": "Den Ilp, Den Ilp, Nr 93", 
       "id": "37312590"
     }, 
     {
       "lat": "4.90948363921402", 
       "lon": "52.4501115865589", 
       "name": "Den Ilp, Den Ilp, Nr 68", 
       "id": "37312610"
     }, 
     {
       "lat": "5.0783631209785", 
       "lon": "52.4363007709105", 
       "name": "Uitdam, Uitdam, Aansluiting Markerdijk", 
       "id": "37391010"
     }, 
     {
       "lat": "4.94439075303077", 
       "lon": "52.5074344334905", 
       "name": "Purmerend, Purmerend, Tramplein", 
       "id": "37400105"
     }, 
     {
       "lat": "4.96718182242481", 
       "lon": "52.4852104821661", 
       "name": "Purmerend, Purmerend, Dom Helder Camarastraat", 
       "id": "37400122"
     }, 
     {
       "lat": "4.9684082710692", 
       "lon": "52.487839154138", 
       "name": "Purmerend, Purmerend, Beethovenstraat", 
       "id": "37400351"
     }, 
     {
       "lat": "4.99355104407387", 
       "lon": "52.5113734084063", 
       "name": "Purmerend, Purmerend, Korenstraat", 
       "id": "37400500"
     }, 
     {
       "lat": "4.99386301492672", 
       "lon": "52.5110778589069", 
       "name": "Purmerend, Purmerend, Korenstraat (uitstaphalte)", 
       "id": "37400501"
     }, 
     {
       "lat": "4.99384612451288", 
       "lon": "52.5113204624555", 
       "name": "Purmerend, Purmerend, Korenstraat", 
       "id": "37400502"
     }, 
     {
       "lat": "4.99316285339002", 
       "lon": "52.5119563004882", 
       "name": "Purmerend, Purmerend, Korenstraat", 
       "id": "37400512"
     }, 
     {
       "lat": "4.94454029036829", 
       "lon": "52.5072103058389", 
       "name": "Purmerend, Purmerend, Tramplein (uitstaphalte)", 
       "id": "37401700"
     }, 
     {
       "lat": "5.07193223495966", 
       "lon": "52.6577843726217", 
       "name": "Hoorn, Hoorn, Oscar Romero", 
       "id": "38110640"
     }, 
     {
       "lat": "5.00177817523921", 
       "lon": "52.5932208106678", 
       "name": "Beets, Beets, N247", 
       "id": "38290340"
     }, 
     {
       "lat": "5.00314651863206", 
       "lon": "52.6004689308447", 
       "name": "Oudendijk, Oudendijk, N247", 
       "id": "38290350"
     }, 
     {
       "lat": "4.90662410822188", 
       "lon": "52.373408596093", 
       "name": "Amsterdam, Amsterdam, Pr. Hendrikkade", 
       "id": "57003020"
     }, 
     {
       "lat": "4.82496659689378", 
       "lon": "52.4217264265012", 
       "name": "zaandam, Zaandam, Zaanderhorn", 
       "id": "37221710"
     }, 
     {
       "lat": "4.83163441797284", 
       "lon": "52.4292625640736", 
       "name": "zaandam, Zaandam, Zweedsestraat", 
       "id": "37222170"
     }, 
     {
       "lat": "4.82959349013319", 
       "lon": "52.4302056687371", 
       "name": "zaandam, Zaandam, Rigastraat", 
       "id": "37222190"
     }, 
     {
       "lat": "4.82051075048731", 
       "lon": "52.4252912769189", 
       "name": "zaandam, Zaandam, Symon Spiersweg", 
       "id": "37222220"
     }, 
     {
       "lat": "4.82093972444216", 
       "lon": "52.4250866114701", 
       "name": "zaandam, Zaandam, Symon Spiersweg", 
       "id": "37222230"
     }, 
     {
       "lat": "4.82548325120954", 
       "lon": "52.4238769272618", 
       "name": "zaandam, Zaandam, Gerrit Kiststraat", 
       "id": "37222240"
     }, 
     {
       "lat": "4.82548906454052", 
       "lon": "52.4234185843066", 
       "name": "zaandam, Zaandam, Gerrit Kiststraat", 
       "id": "37222250"
     }, 
     {
       "lat": "4.82571026699192", 
       "lon": "52.4314815545105", 
       "name": "zaandam, Zaandam, Archangelstraat", 
       "id": "37223110"
     }, 
     {
       "lat": "4.85720651929854", 
       "lon": "52.4204010400194", 
       "name": "zaandam, Zaandam, Achtersluispolder", 
       "id": "37226120"
     }, 
     {
       "lat": "4.69812529112963", 
       "lon": "52.3056165510994", 
       "name": "hoofddorp, Hoofddorp, Draverslaan", 
       "id": "56333210"
     }, 
     {
       "lat": "4.69866033418487", 
       "lon": "52.3051522930988", 
       "name": "hoofddorp, Hoofddorp, Draverslaan", 
       "id": "56333220"
     }, 
     {
       "lat": "4.72744737091646", 
       "lon": "52.2870438675632", 
       "name": "rozenburg, Rozenburg, Kruisweg", 
       "id": "57332321"
     }, 
     {
       "lat": "4.72616101887179", 
       "lon": "52.2878006603575", 
       "name": "rozenburg, Rozenburg, Kruisweg", 
       "id": "57332376"
     }, 
     {
       "lat": "4.73378869793953", 
       "lon": "52.284382691564", 
       "name": "rozenburg, Rozenburg, van Zanten", 
       "id": "57343211"
     }, 
     {
       "lat": "4.73409986922906", 
       "lon": "52.2841507236022", 
       "name": "rozenburg, Rozenburg, van Zanten", 
       "id": "57343221"
     }, 
     {
       "lat": "4.7392683586153", 
       "lon": "52.2834781002046", 
       "name": "rozenburg, Rozenburg, Aalsmeerderweg", 
       "id": "57343231"
     }, 
     {
       "lat": "4.74002578238674", 
       "lon": "52.2827901750439", 
       "name": "rozenburg, Rozenburg, Aalsmeerderweg", 
       "id": "57343241"
     }, 
     {
       "lat": "4.74617824349294", 
       "lon": "52.2799205800246", 
       "name": "schiphol-rijk, Schiphol-Rijk, Beechavenue", 
       "id": "57343251"
     }, 
     {
       "lat": "4.74681944363988", 
       "lon": "52.2791510894935", 
       "name": "schiphol-rijk, Schiphol-Rijk, Beechavenue", 
       "id": "57343261"
     }, 
     {
       "lat": "4.71038461836437", 
       "lon": "52.259300301474", 
       "name": "rijsenhout, Rijsenhout, Rijshornplein", 
       "id": "57542280"
     }, 
     {
       "lat": "4.89013349512967", 
       "lon": "52.3366885040175", 
       "name": "amsterdam, Amsterdam, Station RAI", 
       "id": "57142720"
     }, 
     {
       "lat": "4.82905385752388", 
       "lon": "52.2863088651324", 
       "name": "amstelveen, Amstelveen, Noorddammerweg", 
       "id": "57243900"
     }, 
     {
       "lat": "4.8100136995487", 
       "lon": "52.276303772547", 
       "name": "aalsmeer, Aalsmeer, Nieuw Oosteinde", 
       "id": "57342580"
     }, 
     {
       "lat": "4.80966450779106", 
       "lon": "52.2761133205673", 
       "name": "aalsmeer, Aalsmeer, Nieuw Oosteinde", 
       "id": "57342590"
     }, 
     {
       "lat": "4.75192895458045", 
       "lon": "52.2722938686663", 
       "name": "aalsmeer, Aalsmeer, Dorpsstraat", 
       "id": "57442160"
     }, 
     {
       "lat": "5.03711732595622", 
       "lon": "52.303816181433", 
       "name": "Weesp, Van Houtenlaan", 
       "id": "810012"
     }, 
     {
       "lat": "5.03689783265038", 
       "lon": "52.3037616050935", 
       "name": "Weesp, Van Houtenlaan", 
       "id": "810022"
     }, 
     {
       "lat": "5.03580603819151", 
       "lon": "52.3064816571276", 
       "name": "Weesp, V. Houten Ind.park", 
       "id": "810032"
     }, 
     {
       "lat": "5.03531600390642", 
       "lon": "52.3091136118744", 
       "name": "Weesp, Casparuslaan", 
       "id": "820012"
     }, 
     {
       "lat": "5.03516837767533", 
       "lon": "52.3092390011713", 
       "name": "Weesp, Casparuslaan", 
       "id": "820022"
     }, 
     {
       "lat": "5.03293143457257", 
       "lon": "52.3102569270085", 
       "name": "Weesp, Winkelcentrum", 
       "id": "820032"
     }, 
     {
       "lat": "5.02872284062043", 
       "lon": "52.3102712124268", 
       "name": "Weesp, Sinnigvelderstraat", 
       "id": "820052"
     }, 
     {
       "lat": "5.02964713703842", 
       "lon": "52.3102110953306", 
       "name": "Weesp, Sinnigvelderstraat", 
       "id": "820062"
     }, 
     {
       "lat": "5.02490619813932", 
       "lon": "52.3107718876406", 
       "name": "Weesp, Pampuslaan", 
       "id": "820072"
     }, 
     {
       "lat": "5.02481894998816", 
       "lon": "52.3106817429029", 
       "name": "Weesp, Pampuslaan", 
       "id": "820082"
     }, 
     {
       "lat": "5.02564442525491", 
       "lon": "52.3137580785988", 
       "name": "Weesp, Gemeenschapspolderweg", 
       "id": "820092"
     }, 
     {
       "lat": "5.02543868350128", 
       "lon": "52.3138113761433", 
       "name": "Weesp, Gemeenschapspolderweg", 
       "id": "820102"
     }, 
     {
       "lat": "5.02737155978422", 
       "lon": "52.3141677926712", 
       "name": "Weesp, Verpleegtehuis Hogewey", 
       "id": "820112"
     }, 
     {
       "lat": "5.02902119131481", 
       "lon": "52.3187385701508", 
       "name": "Weesp, Bloemendalerweg", 
       "id": "820132"
     }, 
     {
       "lat": "5.02821920123645", 
       "lon": "52.3181609244787", 
       "name": "Weesp, Bloemendalerweg", 
       "id": "820142"
     }, 
     {
       "lat": "5.04383200957768", 
       "lon": "52.3114484860101", 
       "name": "Weesp, Station Weesp", 
       "id": "820152"
     }, 
     {
       "lat": "5.04407853987405", 
       "lon": "52.302308659416", 
       "name": "Weesp, Molenpad", 
       "id": "820202"
     }, 
     {
       "lat": "5.04682504773611", 
       "lon": "52.2997550828891", 
       "name": "Weesp, Reigersweide", 
       "id": "820222"
     }, 
     {
       "lat": "5.04180683189319", 
       "lon": "52.2984373103311", 
       "name": "Weesp, Sporthal Aetsveld", 
       "id": "820232"
     }, 
     {
       "lat": "5.03856490996709", 
       "lon": "52.3005758751286", 
       "name": "Weesp, Blokland", 
       "id": "820242"
     }, 
     {
       "lat": "5.04452408866651", 
       "lon": "52.3129784085396", 
       "name": "Weesp, L. Eelantsplein", 
       "id": "820252"
     }, 
     {
       "lat": "5.04466996918743", 
       "lon": "52.3130776961103", 
       "name": "Weesp, L. Eelantsplein", 
       "id": "820262"
     }, 
     {
       "lat": "4.9000187421025", 
       "lon": "52.574899570681", 
       "name": "Westbeemster, Westbeemster, Kerkplein", 
       "id": "36470011"
     }, 
     {
       "lat": "4.90001864280355", 
       "lon": "52.5749085575828", 
       "name": "Westbeemster, Westbeemster, Kerkplein", 
       "id": "36470021"
     }, 
     {
       "lat": "4.95388415833712", 
       "lon": "52.5336677232783", 
       "name": "Zuidoostbeemster, Zuidoostbeemster, Kwadijkerweg", 
       "id": "36570200"
     }, 
     {
       "lat": "4.95366309739285", 
       "lon": "52.5336669162054", 
       "name": "Zuidoostbeemster, Zuidoostbeemster, Kwadijkerweg", 
       "id": "36570210"
     }, 
     {
       "lat": "5.0657418166274", 
       "lon": "52.6595112947999", 
       "name": "Hoorn, Hoorn, Blokmergouw", 
       "id": "38111240"
     }, 
     {
       "lat": "4.98442677081534", 
       "lon": "52.5895773636647", 
       "name": "Beets, Beets, Viaduct A7", 
       "id": "38291090"
     }, 
     {
       "lat": "4.9844277563096", 
       "lon": "52.5894695202088", 
       "name": "Beets, Beets, Viaduct A7", 
       "id": "38291100"
     }, 
     {
       "lat": "4.97829714058896", 
       "lon": "52.5885947945039", 
       "name": "Beets, Beets, N.H.Kerk", 
       "id": "38291110"
     }, 
     {
       "lat": "4.97840118137248", 
       "lon": "52.5885142673415", 
       "name": "Beets, Beets, N.H.Kerk", 
       "id": "38291120"
     }, 
     {
       "lat": "4.68610081514775", 
       "lon": "52.2731621022964", 
       "name": "hoofddorp, Hoofddorp, Rijnlanderweg 1058", 
       "id": "57432180"
     }, 
     {
       "lat": "4.68668286987725", 
       "lon": "52.2734172180296", 
       "name": "hoofddorp, Hoofddorp, Rijnlanderweg 1058", 
       "id": "57432190"
     }, 
     {
       "lat": "4.98472899952965", 
       "lon": "52.5273773006294", 
       "name": "Kwadijk, Kwadijk, Durkweg", 
       "id": "36572050"
     }, 
     {
       "lat": "4.98484770116579", 
       "lon": "52.5272878293989", 
       "name": "Kwadijk, Kwadijk, Durkweg", 
       "id": "36572060"
     }, 
     {
       "lat": "4.94001775301944", 
       "lon": "52.5174659644263", 
       "name": "Zuidoostbeemster, Zuidoostbeemster, J.J. Grootlaan", 
       "id": "36573050"
     }, 
     {
       "lat": "4.93988480125809", 
       "lon": "52.5175014130336", 
       "name": "Zuidoostbeemster, Zuidoostbeemster, J.J. Grootlaan", 
       "id": "36573060"
     }, 
     {
       "lat": "4.9446747672532", 
       "lon": "52.5173126591126", 
       "name": "Zuidoostbeemster, Zuidoostbeemster, Middenpad", 
       "id": "36573070"
     }, 
     {
       "lat": "4.94471806269477", 
       "lon": "52.5174026945572", 
       "name": "Zuidoostbeemster, Zuidoostbeemster, Middenpad", 
       "id": "36573080"
     }, 
     {
       "lat": "4.93743070850953", 
       "lon": "52.4951853413282", 
       "name": "Purmerend, Purmerend, Canberrastraat", 
       "id": "37403820"
     }, 
     {
       "lat": "4.93751951289526", 
       "lon": "52.4951407406972", 
       "name": "Purmerend, Purmerend, Canberrastraat", 
       "id": "37403830"
     }, 
     {
       "lat": "4.90021015917961", 
       "lon": "52.3797996063438", 
       "name": "Amsterdam, Amsterdam, CS IJsei", 
       "id": "57005010"
     }, 
     {
       "lat": "4.89984132689697", 
       "lon": "52.3799508797355", 
       "name": "Amsterdam, Amsterdam, CS IJsei", 
       "id": "57005011"
     }, 
     {
       "lat": "4.89953153350857", 
       "lon": "52.3800754320508", 
       "name": "Amsterdam, Amsterdam, CS IJsei", 
       "id": "57005012"
     }, 
     {
       "lat": "4.89917738288926", 
       "lon": "52.3802267638386", 
       "name": "Amsterdam, Amsterdam, CS IJsei", 
       "id": "57005013"
     }, 
     {
       "lat": "4.89932404784379", 
       "lon": "52.3802453435537", 
       "name": "Amsterdam, Amsterdam, CS IJsei", 
       "id": "57005014"
     }, 
     {
       "lat": "4.89957480159399", 
       "lon": "52.3801475117581", 
       "name": "Amsterdam, Amsterdam, CS IJsei", 
       "id": "57005015"
     }, 
     {
       "lat": "4.89978129804159", 
       "lon": "52.3800674726596", 
       "name": "Amsterdam, Amsterdam, CS IJsei", 
       "id": "57005016"
     }, 
     {
       "lat": "4.89997310755227", 
       "lon": "52.3799873727745", 
       "name": "Amsterdam, Amsterdam, CS IJsei", 
       "id": "57005017"
     }, 
     {
       "lat": "4.90020907356082", 
       "lon": "52.3798984664863", 
       "name": "Amsterdam, Amsterdam, CS IJsei", 
       "id": "57005018"
     }, 
     {
       "lat": "4.90047460816939", 
       "lon": "52.3797917058819", 
       "name": "Amsterdam, Amsterdam, CS IJsei", 
       "id": "57005019"
     }, 
     {
       "lat": "4.90021015917961", 
       "lon": "52.3797996063438", 
       "name": "Amsterdam, Amsterdam, CS IJsei", 
       "id": "57005020"
     }, 
     {
       "lat": "4.89984132689697", 
       "lon": "52.3799508797355", 
       "name": "Amsterdam, Amsterdam, CS IJsei", 
       "id": "57005021"
     }, 
     {
       "lat": "4.89953153350857", 
       "lon": "52.3800754320508", 
       "name": "Amsterdam, Amsterdam, CS IJsei", 
       "id": "57005022"
     }, 
     {
       "lat": "4.89895619831591", 
       "lon": "52.3803067413285", 
       "name": "Amsterdam, Amsterdam, CS IJsei", 
       "id": "57005023"
     }, 
     {
       "lat": "4.89932404784379", 
       "lon": "52.3802453435537", 
       "name": "Amsterdam, Amsterdam, CS IJsei", 
       "id": "57005024"
     }, 
     {
       "lat": "4.89957480159399", 
       "lon": "52.3801475117581", 
       "name": "Amsterdam, Amsterdam, CS IJsei", 
       "id": "57005025"
     }, 
     {
       "lat": "4.89978129804159", 
       "lon": "52.3800674726596", 
       "name": "Amsterdam, Amsterdam, CS IJsei", 
       "id": "57005026"
     }, 
     {
       "lat": "4.89997310755227", 
       "lon": "52.3799873727745", 
       "name": "Amsterdam, Amsterdam, CS IJsei", 
       "id": "57005027"
     }, 
     {
       "lat": "4.90020907356082", 
       "lon": "52.3798984664863", 
       "name": "Amsterdam, Amsterdam, CS IJsei", 
       "id": "57005028"
     }, 
     {
       "lat": "4.90047460816939", 
       "lon": "52.3797917058819", 
       "name": "Amsterdam, Amsterdam, CS IJsei", 
       "id": "57005029"
     }, 
     {
       "lat": "4.89751059271696", 
       "lon": "52.378215627244", 
       "name": "Amsterdam, Amsterdam, CS Pr. Hendrik Plantsoen", 
       "id": "57006025"
     }, 
     {
       "lat": "4.89790968195789", 
       "lon": "52.3779835968381", 
       "name": "Amsterdam, Amsterdam, CS Pr. Hendrik Plantsoen", 
       "id": "57006026"
     }, 
     {
       "lat": "4.89814623604381", 
       "lon": "52.377840770896", 
       "name": "Amsterdam, Amsterdam, CS Pr. Hendrik Plantsoen", 
       "id": "57006027"
     }, 
     {
       "lat": "4.911041003593", 
       "lon": "52.38738431399", 
       "name": "Amsterdam, Amsterdam, Meidoornplein", 
       "id": "57114280"
     }, 
     {
       "lat": "4.9117153327613", 
       "lon": "52.3875128505605", 
       "name": "Amsterdam, Amsterdam, Meidoornplein", 
       "id": "57114282"
     }, 
     {
       "lat": "4.82748396168333", 
       "lon": "52.3493062568166", 
       "name": "Amsterdam, Amsterdam, Johan Huizingalaan", 
       "id": "57134200"
     }, 
     {
       "lat": "4.82744084072931", 
       "lon": "52.3492341505461", 
       "name": "Amsterdam, Amsterdam, Johan Huizingalaan", 
       "id": "57134210"
     }, 
     {
       "lat": "4.67841051235618", 
       "lon": "52.3429078863952", 
       "name": "hoofddorp, Hoofddorp, Expo Haarlemmermeer", 
       "id": "56230070"
     }, 
     {
       "lat": "4.67089991325949", 
       "lon": "52.2972487474061", 
       "name": "hoofddorp, Hoofddorp, Toolenburg Oost", 
       "id": "56333101"
     }, 
     {
       "lat": "4.67128175391967", 
       "lon": "52.2972061198053", 
       "name": "hoofddorp, Hoofddorp, Toolenburg Oost", 
       "id": "56333111"
     }, 
     {
       "lat": "4.60617649703015", 
       "lon": "52.2597181359941", 
       "name": "nieuw-vennep, Nieuw-Vennep, Getsewoud P+R", 
       "id": "56431112"
     }, 
     {
       "lat": "4.60597145584307", 
       "lon": "52.2597167806907", 
       "name": "nieuw-vennep, Nieuw-Vennep, Getsewoud P+R", 
       "id": "56431122"
     }, 
     {
       "lat": "4.61367538620897", 
       "lon": "52.2648097898168", 
       "name": "nieuw-vennep, Nieuw-Vennep, Getsewoud Zuid", 
       "id": "56432701"
     }, 
     {
       "lat": "4.89772253941009", 
       "lon": "52.3776412909466", 
       "name": "amsterdam, Amsterdam, Centraal Station", 
       "id": "57002341"
     }, 
     {
       "lat": "4.90204654089798", 
       "lon": "52.3770658976861", 
       "name": "amsterdam, Amsterdam, Centraal Station", 
       "id": "57003121"
     }, 
     {
       "lat": "4.8905663906119", 
       "lon": "52.3438985119465", 
       "name": "amsterdam, Amsterdam, Scheldeplein", 
       "id": "57142370"
     }, 
     {
       "lat": "4.89100390534244", 
       "lon": "52.3441430166417", 
       "name": "amsterdam, Amsterdam, Scheldeplein", 
       "id": "57142380"
     }, 
     {
       "lat": "4.76525196147358", 
       "lon": "52.3473777778297", 
       "name": "lijnden, Lijnden, Melbournestraat", 
       "id": "57230210"
     }, 
     {
       "lat": "4.83126332664165", 
       "lon": "52.2901121667386", 
       "name": "bovenkerk, Bovenkerk, Salamander", 
       "id": "57243950"
     }, 
     {
       "lat": "4.83126501223799", 
       "lon": "52.2899773562627", 
       "name": "bovenkerk, Bovenkerk, Salamander", 
       "id": "57243960"
     }, 
     {
       "lat": "4.71103231648482", 
       "lon": "52.2957144095985", 
       "name": "hoofddorp, Hoofddorp, Kruisweg 737", 
       "id": "57430060"
     }, 
     {
       "lat": "4.81043528646932", 
       "lon": "52.2483083526251", 
       "name": "uithoorn, Uithoorn, Winterkoning", 
       "id": "58442350"
     }, 
     {
       "lat": "4.81021529880527", 
       "lon": "52.2483342425876", 
       "name": "uithoorn, Uithoorn, Winterkoning", 
       "id": "58442360"
     }, 
     {
       "lat": "5.19060597045695", 
       "lon": "52.367434882519", 
       "name": "almere stad, Almere Stad, Station Muziekwijk", 
       "id": "58651070"
     }, 
     {
       "lat": "5.19148536871463", 
       "lon": "52.3677868549399", 
       "name": "almere stad, Almere Stad, Station Muziekwijk", 
       "id": "58651080"
     }, 
     {
       "lat": "5.1936115773445", 
       "lon": "52.3549560479681", 
       "name": "almere stad, Almere Stad, Gooisekant-Oost", 
       "id": "58651110"
     }, 
     {
       "lat": "5.19469648343557", 
       "lon": "52.3552544077089", 
       "name": "almere stad, Almere Stad, Gooisekant-Oost", 
       "id": "58651120"
     }, 
     {
       "lat": "5.18848194756981", 
       "lon": "52.3532129413507", 
       "name": "almere stad, Almere Stad, Gooisekant-Midden", 
       "id": "58651130"
     }, 
     {
       "lat": "5.189405561037", 
       "lon": "52.3534571533146", 
       "name": "almere stad, Almere Stad, Gooisekant-Midden", 
       "id": "58651140"
     }, 
     {
       "lat": "5.03564518164964", 
       "lon": "52.3064272526774", 
       "name": "Weesp, V. Houten Ind.park", 
       "id": "810042"
     }, 
     {
       "lat": "4.67841280833846", 
       "lon": "52.3427640934743", 
       "name": "hoofddorp, Hoofddorp, Expo Haarlemmermeer", 
       "id": "56230060"
     }, 
     {
       "lat": "4.75117395012411", 
       "lon": "52.2728380754383", 
       "name": "aalsmeer, Aalsmeer, Dorpsstraat", 
       "id": "57442131"
     }, 
     {
       "lat": "5.27763712475599", 
       "lon": "52.3939347871783", 
       "name": "almere buiten, Almere Buiten, Station Buiten", 
       "id": "58750065"
     }, 
     {
       "lat": "5.27851985272549", 
       "lon": "52.3934233101975", 
       "name": "almere buiten, Almere Buiten, Station Buiten", 
       "id": "58750075"
     }, 
     {
       "lat": "4.89164776291217", 
       "lon": "52.5623725602359", 
       "name": "Zonegrens, 3637/3647, Zonegrens, 3637/3647", 
       "id": "36377000"
     }, 
     {
       "lat": "4.85776285467732", 
       "lon": "52.5508932624856", 
       "name": "Zonegrens, 3638/3647, Zonegrens, 3638/3647", 
       "id": "36387000"
     }, 
     {
       "lat": "4.85964355039122", 
       "lon": "52.5600687546784", 
       "name": "Zonegrens, 3638/3647 (Westeinde), Zonegrens, 3638/3647 (Westeinde)", 
       "id": "36387010"
     }, 
     {
       "lat": "4.92968543144806", 
       "lon": "52.5349969366148", 
       "name": "Zonegrens, 3647/3657, Zonegrens, 3647/3657", 
       "id": "36477000"
     }, 
     {
       "lat": "4.94206008062562", 
       "lon": "52.5413980454101", 
       "name": "Zonegrens, 3647/3657 (Rijperweg), Zonegrens, 3647/3657 (Rijperweg)", 
       "id": "36477010"
     }, 
     {
       "lat": "4.85840734538285", 
       "lon": "52.5512466423223", 
       "name": "Zonegrens, 3638/3647, Zonegrens, 3638/3647", 
       "id": "36477011"
     }, 
     {
       "lat": "4.89225651979912", 
       "lon": "52.5620066177643", 
       "name": "Zonegrens, 3637/3647, Zonegrens, 3637/3647", 
       "id": "36477012"
     }, 
     {
       "lat": "4.90597617428292", 
       "lon": "52.5372578922611", 
       "name": "Zonegrens, 3647/3657 (Middenweg), Zonegrens, 3647/3657 (Middenweg)", 
       "id": "36477014"
     }, 
     {
       "lat": "4.85955485906728", 
       "lon": "52.5600863353874", 
       "name": "Zonegrens, 3638/3647 (Westeinde), Zonegrens, 3638/3647 (Westeinde)", 
       "id": "36477015"
     }, 
     {
       "lat": "4.96472763950226", 
       "lon": "52.526346153371", 
       "name": "Zonegrens, 3657/3740, Zonegrens, 3657/3740", 
       "id": "36577000"
     }, 
     {
       "lat": "4.93124661755808", 
       "lon": "52.5351018039693", 
       "name": "Zonegrens, 3647/3657, Zonegrens, 3647/3657", 
       "id": "36577011"
     }, 
     {
       "lat": "4.94190823825568", 
       "lon": "52.5418378564025", 
       "name": "Zonegrens, 3647/3657 (Rijperweg), Zonegrens, 3647/3657 (Rijperweg)", 
       "id": "36577012"
     }, 
     {
       "lat": "4.90618319903974", 
       "lon": "52.5371958195615", 
       "name": "Zonegrens, 3647/3657 (Middenweg), Zonegrens, 3647/3657 (Middenweg)", 
       "id": "36577013"
     }, 
     {
       "lat": "4.94248933695901", 
       "lon": "52.5134219304347", 
       "name": "Zonegrens, 3657/3740 (Zuiderweg), Zonegrens, 3657/3740 (Zuiderweg)", 
       "id": "36577014"
     }, 
     {
       "lat": "4.94222427245366", 
       "lon": "52.4110082359298", 
       "name": "Zonegrens, 3720/5711, Zonegrens, 3720/5711", 
       "id": "37207000"
     }, 
     {
       "lat": "4.99831387748363", 
       "lon": "52.4338183082818", 
       "name": "Zonegrens, 3720/3739, Zonegrens, 3720/3739", 
       "id": "37207010"
     }, 
     {
       "lat": "4.95098840829216", 
       "lon": "52.456805494129", 
       "name": "Zonegrens, 3720/3730, Zonegrens, 3720/3730", 
       "id": "37207011"
     }, 
     {
       "lat": "4.91010860697154", 
       "lon": "52.4494490242063", 
       "name": "Zonegrens, 3721/3731, Zonegrens, 3721/3731", 
       "id": "37217000"
     }, 
     {
       "lat": "4.90579639586733", 
       "lon": "52.4226036557769", 
       "name": "Zonegrens, 5711/3721, Zonegrens, 5711/3721", 
       "id": "37217010"
     }, 
     {
       "lat": "4.90995018179529", 
       "lon": "52.4245797552663", 
       "name": "Zonegrens, 5711/3721 (Zuideinde), Zonegrens, 5711/3721 (Zuideinde)", 
       "id": "37217011"
     }, 
     {
       "lat": "4.950372199478", 
       "lon": "52.4566324626796", 
       "name": "Zonegrens, 3720/3730, Zonegrens, 3720/3730", 
       "id": "37307000"
     }, 
     {
       "lat": "4.94888170901719", 
       "lon": "52.4838231176865", 
       "name": "Zonegrens, 3730/3740, Zonegrens, 3730/3740", 
       "id": "37307010"
     }, 
     {
       "lat": "4.93183519754932", 
       "lon": "52.4908949543988", 
       "name": "Zonegrens, 3731/3740, Zonegrens, 3731/3740", 
       "id": "37317000"
     }, 
     {
       "lat": "4.90997787108806", 
       "lon": "52.4492957095706", 
       "name": "Zonegrens, 3721/3731, Zonegrens, 3721/3731", 
       "id": "37317010"
     }, 
     {
       "lat": "4.99727098690115", 
       "lon": "52.433689056573", 
       "name": "Zonegrens, 3720/3739, Zonegrens, 3720/3739", 
       "id": "37397000"
     }, 
     {
       "lat": "5.03290211175959", 
       "lon": "52.4665243729088", 
       "name": "Zonegrens, 3739/3749, Zonegrens, 3739/3749", 
       "id": "37397010"
     }, 
     {
       "lat": "4.98879358912785", 
       "lon": "52.5227535315697", 
       "name": "Zonegrens, 3740/3750 (Nieuwe Gouw), Zonegrens, 3740/3750 (Nieuwe Gouw)", 
       "id": "37407000"
     }, 
     {
       "lat": "4.96574581064364", 
       "lon": "52.5261969873484", 
       "name": "Zonegrens, 3657/3740, Zonegrens, 3657/3740", 
       "id": "37407010"
     }, 
     {
       "lat": "4.94865822325623", 
       "lon": "52.4840919156787", 
       "name": "Zonegrens, 3730/3740, Zonegrens, 3730/3740", 
       "id": "37407012"
     }, 
     {
       "lat": "4.93152638318149", 
       "lon": "52.4908578187885", 
       "name": "Zonegrens, 3731/3740, Zonegrens, 3731/3740", 
       "id": "37407013"
     }, 
     {
       "lat": "5.01491630830295", 
       "lon": "52.5123950131493", 
       "name": "Zonegrens, 3740/3750, Zonegrens, 3740/3750", 
       "id": "37407014"
     }, 
     {
       "lat": "4.94368594623007", 
       "lon": "52.5130848867349", 
       "name": "Zonegrens, 3657/3740 (Zuiderweg), Zonegrens, 3657/3740 (Zuiderweg)", 
       "id": "37407016"
     }, 
     {
       "lat": "5.03254729160266", 
       "lon": "52.4667300240061", 
       "name": "Zonegrens, 3739/3749, Zonegrens, 3739/3749", 
       "id": "37497000"
     }, 
     {
       "lat": "5.03068106033686", 
       "lon": "52.4883122601789", 
       "name": "Zonegrens, 3849/3749, Zonegrens, 3849/3749", 
       "id": "37497010"
     }, 
     {
       "lat": "5.01517979031103", 
       "lon": "52.5125935616412", 
       "name": "Zonegrens, 3740/3750, Zonegrens, 3740/3750", 
       "id": "37507000"
     }, 
     {
       "lat": "5.03560053552543", 
       "lon": "52.5047109726345", 
       "name": "Zonegrens, 3849/3750, Zonegrens, 3849/3750", 
       "id": "37507010"
     }, 
     {
       "lat": "4.99590686192755", 
       "lon": "52.5563898126849", 
       "name": "Zonegrens, 3750/3829 (Seevancksweg), Zonegrens, 3750/3829 (Seevancksweg)", 
       "id": "37507013"
     }, 
     {
       "lat": "4.97791126849098", 
       "lon": "52.5554573906739", 
       "name": "Zonegrens, 3750/3829 (Westeinde), Zonegrens, 3750/3829 (Westeinde)", 
       "id": "37507014"
     }, 
     {
       "lat": "4.98776295435961", 
       "lon": "52.5226691815486", 
       "name": "Zonegrens, 3740/3750 (Nieuwe Gouw), Zonegrens, 3740/3750 (Nieuwe Gouw)", 
       "id": "37507015"
     }, 
     {
       "lat": "5.01687692261546", 
       "lon": "52.6299185030055", 
       "name": "Zonegrens, 3800/3819, Zonegrens, 3800/3819", 
       "id": "38007000"
     }, 
     {
       "lat": "5.00313175881526", 
       "lon": "52.6004688831494", 
       "name": "Zonegrens, 3819/3829, Zonegrens, 3819/3829", 
       "id": "38197000"
     }, 
     {
       "lat": "5.01701226819716", 
       "lon": "52.6296313362242", 
       "name": "Zonegrens, 3800/3819, Zonegrens, 3800/3819", 
       "id": "38197010"
     }, 
     {
       "lat": "5.00910580546925", 
       "lon": "52.5613486101131", 
       "name": "Zonegrens, 3829/3839, Zonegrens, 3829/3839", 
       "id": "38297000"
     }, 
     {
       "lat": "5.00363919936788", 
       "lon": "52.6015220242073", 
       "name": "Zonegrens, 3819/3829, Zonegrens, 3819/3829", 
       "id": "38297010"
     }, 
     {
       "lat": "4.99503418788795", 
       "lon": "52.5566925024128", 
       "name": "Zonegrens, 3750/3829 (Seevancksweg), Zonegrens, 3750/3829 (Seevancksweg)", 
       "id": "38297013"
     }, 
     {
       "lat": "4.9775748935429", 
       "lon": "52.5551596497882", 
       "name": "Zonegrens, 3750/3829 (Westeinde), Zonegrens, 3750/3829 (Westeinde)", 
       "id": "38297014"
     }, 
     {
       "lat": "5.04544467916936", 
       "lon": "52.5153987501594", 
       "name": "Zonegrens, 3839/3849, Zonegrens, 3839/3849", 
       "id": "38397000"
     }, 
     {
       "lat": "5.00831303653331", 
       "lon": "52.5626492394326", 
       "name": "Zonegrens, 3829/3839, Zonegrens, 3829/3839", 
       "id": "38397010"
     }, 
     {
       "lat": "5.03044542975166", 
       "lon": "52.4883205392872", 
       "name": "Zonegrens, 3849/3749, Zonegrens, 3849/3749", 
       "id": "38497000"
     }, 
     {
       "lat": "5.04579496905841", 
       "lon": "52.5158221640569", 
       "name": "Zonegrens, 3839/3849, Zonegrens, 3839/3849", 
       "id": "38497010"
     }, 
     {
       "lat": "5.03927364459569", 
       "lon": "52.5039758454821", 
       "name": "Zonegrens, 3849/3750, Zonegrens, 3849/3750", 
       "id": "38497011"
     }, 
     {
       "lat": "4.91202720498581", 
       "lon": "52.3721181981946", 
       "name": "Zonegrens, 5700/5711, Zonegrens, 5700/5711", 
       "id": "57007000"
     }, 
     {
       "lat": "4.97012029535655", 
       "lon": "52.3640594254947", 
       "name": "Zonegrens, 5715/5710, Zonegrens, 5715/5710", 
       "id": "57107000"
     }, 
     {
       "lat": "4.97411931843243", 
       "lon": "52.3776448242535", 
       "name": "Zonegrens, 5711/5710, Zonegrens, 5711/5710", 
       "id": "57107010"
     }, 
     {
       "lat": "4.97316324841948", 
       "lon": "52.3778032632524", 
       "name": "Zonegrens, 5711/5710, Zonegrens, 5711/5710", 
       "id": "57117000"
     }, 
     {
       "lat": "4.94300228856726", 
       "lon": "52.4111010314096", 
       "name": "Zonegrens, 3720/5711, Zonegrens, 3720/5711", 
       "id": "57117010"
     }, 
     {
       "lat": "4.91283381288208", 
       "lon": "52.3859444931358", 
       "name": "Zonegrens, 5700/5711, Zonegrens, 5700/5711", 
       "id": "57117011"
     }, 
     {
       "lat": "4.90629532906379", 
       "lon": "52.4226865700907", 
       "name": "Zonegrens, 5711/3721, Zonegrens, 5711/3721", 
       "id": "57117012"
     }, 
     {
       "lat": "4.91037834918017", 
       "lon": "52.4244107143802", 
       "name": "Zonegrens, 5711/3721 (Zuideinde), Zonegrens, 5711/3721 (Zuideinde)", 
       "id": "57117013"
     }, 
     {
       "lat": "4.88040342729427", 
       "lon": "52.4242683381127", 
       "name": "Zonegrens, 5711/5712, Zonegrens, 5711/5712", 
       "id": "57117014"
     }, 
     {
       "lat": "4.88032036516025", 
       "lon": "52.4238186017914", 
       "name": "Zonegrens, 5711/5712, Zonegrens, 5711/5712", 
       "id": "57127000"
     }, 
     {
       "lat": "4.84359787345893", 
       "lon": "52.3901407862384", 
       "name": "Zonegrens, 5712/5713, Zonegrens, 5712/5713", 
       "id": "57127010"
     }, 
     {
       "lat": "4.8448492256585", 
       "lon": "52.3899218305362", 
       "name": "Zonegrens, 5712/5713, Zonegrens, 5712/5713", 
       "id": "57137000"
     }, 
     {
       "lat": "4.97531222942732", 
       "lon": "52.3314162663883", 
       "name": "Zonegrens, 5725/5715, Zonegrens, 5725/5715", 
       "id": "57157000"
     }, 
     {
       "lat": "4.97064720945884", 
       "lon": "52.3642320464577", 
       "name": "Zonegrens, 5715/5710, Zonegrens, 5715/5710", 
       "id": "57157010"
     }, 
     {
       "lat": "4.97573849918667", 
       "lon": "52.3313278719462", 
       "name": "Zonegrens, 5725/5715, Zonegrens, 5725/5715", 
       "id": "57257010"
     }, 
     {
       "lat": "5.01391129011539", 
       "lon": "52.348818687421", 
       "name": "Amsterdam, IJburg (Strand)", 
       "id": "82222"
     }, 
     {
       "lat": "5.01404586763741", 
       "lon": "52.3485225179837", 
       "name": "Amsterdam, IJburg (Strand)", 
       "id": "82232"
     }, 
     {
       "lat": "4.9521232684699", 
       "lon": "52.3548182166301", 
       "name": "Amsterdam, Science Park A'dam", 
       "id": "4912"
     }, 
     {
       "lat": "4.95428333174545", 
       "lon": "52.3560844147321", 
       "name": "Amsterdam, Science Park Aqua", 
       "id": "4942"
     }, 
     {
       "lat": "4.960195604941", 
       "lon": "52.3564294455613", 
       "name": "Amsterdam, Science Park Ignis", 
       "id": "4982"
     }, 
     {
       "lat": "4.95897813437527", 
       "lon": "52.3548162489521", 
       "name": "Amsterdam, Science Park Aer", 
       "id": "5002"
     }, 
     {
       "lat": "4.95653912534468", 
       "lon": "52.3535491219089", 
       "name": "Amsterdam, Science Park Terra", 
       "id": "5022"
     }, 
     {
       "lat": "4.83670469067099", 
       "lon": "52.2744357579998", 
       "name": "amstelveen, Amstelveen, Burg. Wiegelweg", 
       "id": "57240090"
     }, 
     {
       "lat": "5.06928504417579", 
       "lon": "52.6559709311729", 
       "name": "Zonegrens, 3800/3811 (Nieuwesteen), Zonegrens, 3800/3811 (Nieuwesteen)", 
       "id": "38007011"
     }, 
     {
       "lat": "5.06922541042427", 
       "lon": "52.6560426682226", 
       "name": "Zonegrens, 3800/3811 (Nieuwesteen), Zonegrens, 3800/3811 (Nieuwesteen)", 
       "id": "38117011"
     }, 
     {
       "lat": "4.83255635009973", 
       "lon": "52.3803019604309", 
       "name": "Amsterdam, Burg. Fockstraat", 
       "id": "30532"
     }, 
     {
       "lat": "4.81458855613429", 
       "lon": "52.4387263054444", 
       "name": "zaandam, Zaandam, Station", 
       "id": "37220130"
     }, 
     {
       "lat": "4.81438453959282", 
       "lon": "52.438581517452", 
       "name": "zaandam, Zaandam, Station", 
       "id": "37220131"
     }, 
     {
       "lat": "4.81470864100114", 
       "lon": "52.4385381451774", 
       "name": "zaandam, Zaandam, Station", 
       "id": "37220132"
     }, 
     {
       "lat": "4.81414390047951", 
       "lon": "52.4389937854835", 
       "name": "zaandam, Zaandam, Station", 
       "id": "37220134"
     }, 
     {
       "lat": "4.8142791587599", 
       "lon": "52.4387697484707", 
       "name": "zaandam, Zaandam, Station", 
       "id": "37220137"
     }, 
     {
       "lat": "4.81431873943704", 
       "lon": "52.4391204575794", 
       "name": "zaandam, Zaandam, Station", 
       "id": "37220139"
     }, 
     {
       "lat": "4.77626124962888", 
       "lon": "52.4356948380349", 
       "name": "westzaan, Westzaan, Lexion", 
       "id": "37220610"
     }, 
     {
       "lat": "4.77621477974868", 
       "lon": "52.4358653641852", 
       "name": "westzaan, Westzaan, Lexion", 
       "id": "37220620"
     }, 
     {
       "lat": "4.8259162174093", 
       "lon": "52.4535111890862", 
       "name": "zaandam, Zaandam, Zaans Medisch Centrum", 
       "id": "37220860"
     }, 
     {
       "lat": "4.81397829846365", 
       "lon": "52.4392895766714", 
       "name": "zaandam, Zaandam, Station", 
       "id": "37220911"
     }, 
     {
       "lat": "4.81445364838784", 
       "lon": "52.4389233815937", 
       "name": "zaandam, Zaandam, Station", 
       "id": "37220912"
     }, 
     {
       "lat": "4.81418382928188", 
       "lon": "52.4393175334015", 
       "name": "zaandam, Zaandam, Station", 
       "id": "37220914"
     }, 
     {
       "lat": "4.81399137493504", 
       "lon": "52.4394154668038", 
       "name": "zaandam, Zaandam, Station", 
       "id": "37220917"
     }, 
     {
       "lat": "4.83687835820682", 
       "lon": "52.423759630566", 
       "name": "zaandam, Zaandam, Haven 132", 
       "id": "37221010"
     }, 
     {
       "lat": "4.83679093651791", 
       "lon": "52.4236963109877", 
       "name": "zaandam, Zaandam, Haven 132", 
       "id": "37221080"
     }, 
     {
       "lat": "4.839297187697", 
       "lon": "52.4540231645693", 
       "name": "zaandam, Zaandam, Noordwachter", 
       "id": "37221720"
     }, 
     {
       "lat": "4.83921159499599", 
       "lon": "52.4538070668071", 
       "name": "zaandam, Zaandam, Noordwachter", 
       "id": "37221730"
     }, 
     {
       "lat": "4.85478863715549", 
       "lon": "52.43443786751", 
       "name": "zaandam, Zaandam, Weerpad/Wachterstraat", 
       "id": "37221740"
     }, 
     {
       "lat": "4.85451001481747", 
       "lon": "52.434373702233", 
       "name": "zaandam, Zaandam, Weerpad/Wachterstraat", 
       "id": "37221750"
     }, 
     {
       "lat": "4.83279966159469", 
       "lon": "52.454801841581", 
       "name": "zaandam, Zaandam, Tjalkstraat", 
       "id": "37221760"
     }, 
     {
       "lat": "4.83179616209454", 
       "lon": "52.4550487973156", 
       "name": "ONBEKEND, Zaandam , Tjalkstraat", 
       "id": "37221770"
     }, 
     {
       "lat": "4.78824614978213", 
       "lon": "52.4291770409721", 
       "name": "zaandam, Zaandam, Willem Hooftkade", 
       "id": "37222260"
     }, 
     {
       "lat": "4.78831929656495", 
       "lon": "52.4292043736704", 
       "name": "zaandam, Zaandam, Willem Hooftkade", 
       "id": "37222270"
     }, 
     {
       "lat": "4.83443549327923", 
       "lon": "52.4263097401514", 
       "name": "zaandam, Zaandam, Delftse Rij", 
       "id": "37222280"
     }, 
     {
       "lat": "4.82689717184634", 
       "lon": "52.4213491017099", 
       "name": "zaandam, Zaandam, Hemkade/Pont", 
       "id": "37223010"
     }, 
     {
       "lat": "4.82694229430668", 
       "lon": "52.4212684261226", 
       "name": "zaandam, Zaandam, Hemkade/Pont", 
       "id": "37223020"
     }, 
     {
       "lat": "4.83312968208813", 
       "lon": "52.42021900099", 
       "name": "zaandam, Zaandam, Hemkade", 
       "id": "37223030"
     }, 
     {
       "lat": "4.8333074236278", 
       "lon": "52.4201119800871", 
       "name": "zaandam, Zaandam, Hemkade", 
       "id": "37223040"
     }, 
     {
       "lat": "4.85624049987482", 
       "lon": "52.4298606940339", 
       "name": "zaandam, Zaandam, De Vlinder", 
       "id": "37223554"
     }, 
     {
       "lat": "4.85667118391595", 
       "lon": "52.429503117821", 
       "name": "zaandam, Zaandam, De Vlinder", 
       "id": "37223601"
     }, 
     {
       "lat": "4.75790751998169", 
       "lon": "52.4885359558521", 
       "name": "assendelft, Assendelft, Ambachtslaan", 
       "id": "37320380"
     }, 
     {
       "lat": "4.75786578525393", 
       "lon": "52.4883649704029", 
       "name": "assendelft, Assendelft, Ambachtslaan", 
       "id": "37320390"
     }, 
     {
       "lat": "4.75387635772323", 
       "lon": "52.4400262338913", 
       "name": "nauerna, Nauerna, Sluisbrug", 
       "id": "37330310"
     }, 
     {
       "lat": "4.72553536573542", 
       "lon": "52.4351528605565", 
       "name": "nauerna, Nauerna, Pont Buitenhuizen", 
       "id": "37330370"
     }, 
     {
       "lat": "4.75384514583221", 
       "lon": "52.4401518945894", 
       "name": "nauerna, Nauerna, Sluisbrug", 
       "id": "37330380"
     }, 
     {
       "lat": "4.89833724632384", 
       "lon": "52.3778325719148", 
       "name": "amsterdam, Amsterdam, Centraal Station", 
       "id": "57000321"
     }, 
     {
       "lat": "4.90762368445229", 
       "lon": "52.3991174005936", 
       "name": "amsterdam, Amsterdam, Slijperweg", 
       "id": "57113290"
     }, 
     {
       "lat": "4.90718290809981", 
       "lon": "52.3991156152721", 
       "name": "amsterdam, Amsterdam, Slijperweg", 
       "id": "57113860"
     }, 
     {
       "lat": "4.83881565955067", 
       "lon": "52.3884020866928", 
       "name": "amsterdam, Amsterdam, Station Sloterdijk", 
       "id": "57125010"
     }, 
     {
       "lat": "4.84645989714362", 
       "lon": "52.3771037219478", 
       "name": "amsterdam, Amsterdam, Bos en Lommerplein", 
       "id": "57130850"
     }, 
     {
       "lat": "4.83862319860475", 
       "lon": "52.3695269595276", 
       "name": "amsterdam, Amsterdam, Jan Voermanstraat", 
       "id": "57134750"
     }, 
     {
       "lat": "4.83866858005531", 
       "lon": "52.3694193168081", 
       "name": "amsterdam, Amsterdam, Jan Voermanstraat", 
       "id": "57134760"
     }, 
     {
       "lat": "4.8250904752635", 
       "lon": "52.3401273553794", 
       "name": "amsterdam, Amsterdam, John M. Keynesplein", 
       "id": "57134770"
     }, 
     {
       "lat": "4.92077083185829", 
       "lon": "52.3254077497653", 
       "name": "Amsterdam, Flinesstraat", 
       "id": "5752"
     }, 
     {
       "lat": "4.92038832595658", 
       "lon": "52.3255140945813", 
       "name": "Amsterdam, Flinesstraat", 
       "id": "5762"
     }, 
     {
       "lat": "4.90590243602181", 
       "lon": "52.3925494285933", 
       "name": "Amsterdam, Chrysantenstraat", 
       "id": "11402"
     }, 
     {
       "lat": "4.90566856165211", 
       "lon": "52.3924406260313", 
       "name": "Amsterdam, Chrysantenstraat", 
       "id": "12732"
     }, 
     {
       "lat": "4.90657371531667", 
       "lon": "52.3983851451996", 
       "name": "Amsterdam, Klaprozenweg", 
       "id": "14012"
     }, 
     {
       "lat": "4.90614100565034", 
       "lon": "52.3989945491395", 
       "name": "Amsterdam, Klaprozenweg", 
       "id": "14022"
     }, 
     {
       "lat": "4.90267832703222", 
       "lon": "52.3945135698064", 
       "name": "Amsterdam, Distelweg", 
       "id": "14032"
     }, 
     {
       "lat": "4.90238450682844", 
       "lon": "52.3945123675392", 
       "name": "Amsterdam, Distelweg", 
       "id": "14042"
     }, 
     {
       "lat": "4.83931474779202", 
       "lon": "52.3884313597719", 
       "name": "Amsterdam, Station Sloterdijk", 
       "id": "23611"
     }, 
     {
       "lat": "4.83878594830416", 
       "lon": "52.3884289122552", 
       "name": "Amsterdam, Station Sloterdijk", 
       "id": "23642"
     }, 
     {
       "lat": "4.8387293053013", 
       "lon": "52.3882578833785", 
       "name": "Amsterdam, Station Sloterdijk", 
       "id": "23652"
     }, 
     {
       "lat": "4.83856895169142", 
       "lon": "52.388158275787", 
       "name": "Amsterdam, Station Sloterdijk", 
       "id": "23662"
     }, 
     {
       "lat": "4.83857061991759", 
       "lon": "52.3880234677951", 
       "name": "Amsterdam, Station Sloterdijk", 
       "id": "23672"
     }, 
     {
       "lat": "4.83860199914436", 
       "lon": "52.3878618342873", 
       "name": "Amsterdam, Station Sloterdijk", 
       "id": "23692"
     }, 
     {
       "lat": "4.83845611342878", 
       "lon": "52.3877802689783", 
       "name": "Amsterdam, Station Sloterdijk", 
       "id": "23702"
     }, 
     {
       "lat": "4.83888452983963", 
       "lon": "52.3875845235392", 
       "name": "Amsterdam, Station Sloterdijk", 
       "id": "23712"
     }, 
     {
       "lat": "4.83859654077483", 
       "lon": "52.3871158285947", 
       "name": "Amsterdam, Station Sloterdijk", 
       "id": "23732"
     }, 
     {
       "lat": "4.83852343224835", 
       "lon": "52.3870885267567", 
       "name": "Amsterdam, Station Sloterdijk", 
       "id": "23742"
     }, 
     {
       "lat": "4.83377918457703", 
       "lon": "52.3870574639208", 
       "name": "Amsterdam, Barajasweg", 
       "id": "23752"
     }, 
     {
       "lat": "4.83366201392552", 
       "lon": "52.3870299531571", 
       "name": "Amsterdam, Barajasweg", 
       "id": "23762"
     }, 
     {
       "lat": "4.85787601958036", 
       "lon": "52.3028262914957", 
       "name": "Amstelveen, Busstation A'veen", 
       "id": "75352"
     }, 
     {
       "lat": "4.85742743263521", 
       "lon": "52.302329950957", 
       "name": "Amstelveen, Busstation A'veen", 
       "id": "79632"
     }, 
     {
       "lat": "4.91234122166772", 
       "lon": "52.3537575556049", 
       "name": "Amsterdam, Platanenweg", 
       "id": "91722"
     }, 
     {
       "lat": "4.91261214454601", 
       "lon": "52.3531295008733", 
       "name": "Amsterdam, Platanenweg", 
       "id": "91732"
     }, 
     {
       "lat": "4.56051823349719", 
       "lon": "52.2188168354053", 
       "name": "buitenkaag, Buitenkaag, Kaagpont", 
       "id": "56337101"
     }, 
     {
       "lat": "4.56056229690402", 
       "lon": "52.2188081556089", 
       "name": "buitenkaag, Buitenkaag, Kaagpont", 
       "id": "56337102"
     }, 
     {
       "lat": "4.56051840026183", 
       "lon": "52.2188078483379", 
       "name": "buitenkaag, Buitenkaag, Kaagpont", 
       "id": "56337103"
     }, 
     {
       "lat": "4.56026655468323", 
       "lon": "52.2205498024642", 
       "name": "buitenkaag, Buitenkaag, Eimerstraat", 
       "id": "56537070"
     }, 
     {
       "lat": "4.56025158824399", 
       "lon": "52.2205676741328", 
       "name": "buitenkaag, Buitenkaag, Eimerstraat", 
       "id": "56537080"
     }, 
     {
       "lat": "4.56047417007328", 
       "lon": "52.2188255151853", 
       "name": "buitenkaag, Buitenkaag, Kaagpont", 
       "id": "56537100"
     }, 
     {
       "lat": "4.83890099677319", 
       "lon": "52.3874407963302", 
       "name": "amsterdam, Amsterdam, Station Sloterdijk", 
       "id": "57135179"
     }, 
     {
       "lat": "4.87808038801581", 
       "lon": "52.295059611085", 
       "name": "amstelveen, Amstelveen, Langerhuize", 
       "id": "57240160"
     }, 
     {
       "lat": "4.87863718949466", 
       "lon": "52.2950799826131", 
       "name": "amstelveen, Amstelveen, Langerhuize", 
       "id": "57240170"
     }, 
     {
       "lat": "4.97135503216174", 
       "lon": "52.2745816204412", 
       "name": "abcoude, Abcoude, Broekzijdselaan", 
       "id": "57352270"
     }, 
     {
       "lat": "4.82084348504908", 
       "lon": "52.2428131162324", 
       "name": "uithoorn, Uithoorn, Busstation", 
       "id": "58442061"
     }, 
     {
       "lat": "4.82101860275496", 
       "lon": "52.242858895397", 
       "name": "uithoorn, Uithoorn, Busstation", 
       "id": "58442062"
     }, 
     {
       "lat": "4.82091588870479", 
       "lon": "52.2428763791209", 
       "name": "uithoorn, Uithoorn, Busstation", 
       "id": "58442063"
     }, 
     {
       "lat": "4.82109066391707", 
       "lon": "52.2429491204729", 
       "name": "uithoorn, Uithoorn, Busstation", 
       "id": "58442064"
     }, 
     {
       "lat": "4.82098794968663", 
       "lon": "52.242966604259", 
       "name": "uithoorn, Uithoorn, Busstation", 
       "id": "58442065"
     }, 
     {
       "lat": "4.82119212129576", 
       "lon": "52.2430304983459", 
       "name": "uithoorn, Uithoorn, Busstation", 
       "id": "58442066"
     }, 
     {
       "lat": "4.82108906409759", 
       "lon": "52.2430749445139", 
       "name": "uithoorn, Uithoorn, Busstation", 
       "id": "58442067"
     }, 
     {
       "lat": "4.82127916665463", 
       "lon": "52.2430938311445", 
       "name": "uithoorn, Uithoorn, Busstation", 
       "id": "58442068"
     }, 
     {
       "lat": "4.83422850891907", 
       "lon": "52.2355333399118", 
       "name": "uithoorn, Uithoorn, Stationsstraat", 
       "id": "58442160"
     }, 
     {
       "lat": "4.83492119465301", 
       "lon": "52.2351590847754", 
       "name": "uithoorn, Uithoorn, Stationsstraat", 
       "id": "58442170"
     }, 
     {
       "lat": "4.84981013373431", 
       "lon": "52.5598449176978", 
       "name": "De Rijp, De Rijp, Grote Dam", 
       "id": "36380020"
     }, 
     {
       "lat": "4.84666509384426", 
       "lon": "52.5565592393251", 
       "name": "De Rijp, De Rijp, Bernhardstraat", 
       "id": "36380030"
     }, 
     {
       "lat": "4.95638926435639", 
       "lon": "52.5382334311282", 
       "name": "Zuidoostbeemster, Zuidoostbeemster, Rijperwg/Purmerenderwg", 
       "id": "36570191"
     }, 
     {
       "lat": "4.92101493781106", 
       "lon": "52.4320924857627", 
       "name": "Landsmeer, Landsmeer, Goudpluvier", 
       "id": "37212310"
     }, 
     {
       "lat": "4.91467791975987", 
       "lon": "52.4320494152496", 
       "name": "Landsmeer, Landsmeer, Raadhuisstraat", 
       "id": "37212330"
     }, 
     {
       "lat": "4.91922319922661", 
       "lon": "52.4318876978014", 
       "name": "Landsmeer, Landsmeer, Roerdompstraat", 
       "id": "37212810"
     }, 
     {
       "lat": "5.07231902532872", 
       "lon": "52.5066205383741", 
       "name": "Volendam, Volendam, Grote Ven", 
       "id": "38490670"
     }, 
     {
       "lat": "5.07213767853659", 
       "lon": "52.5052000530731", 
       "name": "Volendam, Volendam, Grote Ven", 
       "id": "38490680"
     }, 
     {
       "lat": "4.97450289613213", 
       "lon": "52.2716716027868", 
       "name": "abcoude, Abcoude, Hoogstraat", 
       "id": "57352021"
     }, 
     {
       "lat": "4.97246771833988", 
       "lon": "52.2731025354272", 
       "name": "abcoude, Abcoude, Dr. van Doornplein", 
       "id": "57352061"
     }, 
     {
       "lat": "4.97284679451732", 
       "lon": "52.2685829791307", 
       "name": "abcoude, Abcoude, Burg. des Tombeweg", 
       "id": "57352181"
     }, 
     {
       "lat": "4.87898953161201", 
       "lon": "52.3809237760664", 
       "name": "Amsterdam, Nassaukade", 
       "id": "23352"
     }, 
     {
       "lat": "4.48186451582244", 
       "lon": "52.1652716537747", 
       "name": "leiden, Leiden, Centraal Station", 
       "id": "54444256"
     }, 
     {
       "lat": "4.81084794777387", 
       "lon": "52.3091676144363", 
       "name": "schiphol oost, Schiphol Oost, Poortstraat", 
       "id": "57340290"
     }, 
     {
       "lat": "4.81067397876678", 
       "lon": "52.3090139727217", 
       "name": "schiphol oost, Schiphol Oost, Poortstraat", 
       "id": "57340300"
     }, 
     {
       "lat": "4.88292191247948", 
       "lon": "52.3450885226371", 
       "name": "Amsterdam, G. Gezellestraat", 
       "id": "74872"
     }, 
     {
       "lat": "4.89010665899815", 
       "lon": "52.3443279944627", 
       "name": "Amsterdam, Scheldeplein", 
       "id": "95562"
     }, 
     {
       "lat": "4.88246638645277", 
       "lon": "52.345140507432", 
       "name": "Amsterdam, G. Gezellestraat", 
       "id": "74892"
     }, 
     {
       "lat": "4.75400810195668", 
       "lon": "52.4935212851917", 
       "name": "assendelft, Assendelft, waypoint 2 Saendelverlaan", 
       "id": "37329940"
     }, 
     {
       "lat": "4.79218875350576", 
       "lon": "52.2516512927655", 
       "name": "uithoorn, Uithoorn, Poelweg", 
       "id": "57442400"
     }, 
     {
       "lat": "4.79354123979842", 
       "lon": "52.2512626237962", 
       "name": "uithoorn, Uithoorn, Poelweg", 
       "id": "58442370"
     }, 
     {
       "lat": "4.80260637799786", 
       "lon": "52.2490158826056", 
       "name": "uithoorn, Uithoorn, Noorddammerweg", 
       "id": "58442520"
     }, 
     {
       "lat": "4.80306419548455", 
       "lon": "52.2487215432578", 
       "name": "uithoorn, Uithoorn, Noorddammerweg", 
       "id": "58442530"
     }, 
     {
       "lat": "4.81394006025074", 
       "lon": "52.2456469902839", 
       "name": "uithoorn, Uithoorn, Burg. Kootlaan", 
       "id": "58442590"
     }, 
     {
       "lat": "4.81377622357955", 
       "lon": "52.2458619068135", 
       "name": "uithoorn, Uithoorn, Burg. Kootlaan", 
       "id": "58442600"
     }, 
     {
       "lat": "4.93287187906599", 
       "lon": "52.3613249008019", 
       "name": "Muiderpoortstation, Amsterdam", 
       "id": "000012"
     }, 
     {
       "lat": "4.93279958315244", 
       "lon": "52.3612167708509", 
       "name": "Muiderpoortstation, Amsterdam", 
       "id": "000051"
     }, 
     {
       "lat": "4.93279958315244", 
       "lon": "52.3612167708509", 
       "name": "Muiderpoortstation, Amsterdam", 
       "id": "000052"
     }, 
     {
       "lat": "4.93368203863872", 
       "lon": "52.3610583759296", 
       "name": "Muiderpoortstation, Amsterdam", 
       "id": "000062"
     }, 
     {
       "lat": "4.93356340433637", 
       "lon": "52.3611747615934", 
       "name": "Muiderpoortstation, Amsterdam", 
       "id": "000071"
     }, 
     {
       "lat": "4.93356340433637", 
       "lon": "52.3611747615934", 
       "name": "Muiderpoortstation, Amsterdam", 
       "id": "000072"
     }, 
     {
       "lat": "4.92977651637397", 
       "lon": "52.3611062641378", 
       "name": "Dapperstraat, Amsterdam", 
       "id": "000081"
     }, 
     {
       "lat": "4.92977651637397", 
       "lon": "52.3611062641378", 
       "name": "Dapperstraat, Amsterdam", 
       "id": "000082"
     }, 
     {
       "lat": "4.92891225340736", 
       "lon": "52.3609231674453", 
       "name": "Dapperstraat, Amsterdam", 
       "id": "000101"
     }, 
     {
       "lat": "4.92891225340736", 
       "lon": "52.3609231674453", 
       "name": "Dapperstraat, Amsterdam", 
       "id": "000102"
     }, 
     {
       "lat": "4.92507275897998", 
       "lon": "52.3602701144258", 
       "name": "Wijttenbachstraat, Amsterdam", 
       "id": "000141"
     }, 
     {
       "lat": "4.92507275897998", 
       "lon": "52.3602701144258", 
       "name": "Wijttenbachstraat, Amsterdam", 
       "id": "000142"
     }, 
     {
       "lat": "4.92573484126745", 
       "lon": "52.3601288936787", 
       "name": "Linnaeusstraat, Amsterdam", 
       "id": "000171"
     }, 
     {
       "lat": "4.92573484126745", 
       "lon": "52.3601288936787", 
       "name": "Linnaeusstraat, Amsterdam", 
       "id": "000172"
     }, 
     {
       "lat": "4.91674717483751", 
       "lon": "52.3590599305853", 
       "name": "Beukenweg, Amsterdam", 
       "id": "000201"
     }, 
     {
       "lat": "4.91721032389691", 
       "lon": "52.3582978140296", 
       "name": "Beukenweg, Amsterdam", 
       "id": "000211"
     }, 
     {
       "lat": "4.91808997345505", 
       "lon": "52.3570160589325", 
       "name": "Beukenplein, Amsterdam", 
       "id": "000232"
     }, 
     {
       "lat": "4.91807282463334", 
       "lon": "52.3572496717598", 
       "name": "Beukenplein, Amsterdam", 
       "id": "000242"
     }, 
     {
       "lat": "4.92719053897128", 
       "lon": "52.3570697483089", 
       "name": "Pretoriusstraat, Amsterdam", 
       "id": "000291"
     }, 
     {
       "lat": "4.92719053897128", 
       "lon": "52.3570697483089", 
       "name": "Pretoriusstraat, Amsterdam", 
       "id": "000292"
     }, 
     {
       "lat": "4.92693764626617", 
       "lon": "52.3573923231482", 
       "name": "Pretoriusstraat, Amsterdam", 
       "id": "000301"
     }, 
     {
       "lat": "4.92693764626617", 
       "lon": "52.3573923231482", 
       "name": "Pretoriusstraat, Amsterdam", 
       "id": "000302"
     }, 
     {
       "lat": "4.93083753269626", 
       "lon": "52.3535786536985", 
       "name": "Hogeweg, Amsterdam", 
       "id": "000391"
     }, 
     {
       "lat": "4.93083753269626", 
       "lon": "52.3535786536985", 
       "name": "Hogeweg, Amsterdam", 
       "id": "000392"
     }, 
     {
       "lat": "4.93135502992193", 
       "lon": "52.3532121510784", 
       "name": "Hogeweg, Amsterdam", 
       "id": "000401"
     }, 
     {
       "lat": "4.93135502992193", 
       "lon": "52.3532121510784", 
       "name": "Hogeweg, Amsterdam", 
       "id": "000402"
     }, 
     {
       "lat": "4.93019011097066", 
       "lon": "52.3480307282426", 
       "name": "Maxwellstraat, Amsterdam", 
       "id": "000412"
     }, 
     {
       "lat": "4.93137127234361", 
       "lon": "52.3487722768797", 
       "name": "Pieter Zeemanlaan, Amsterdam", 
       "id": "000422"
     }, 
     {
       "lat": "4.93151812374362", 
       "lon": "52.3487638545964", 
       "name": "Pieter Zeemanlaan, Amsterdam", 
       "id": "000432"
     }, 
     {
       "lat": "4.92432635191824", 
       "lon": "52.3459767136508", 
       "name": "Fizeaustraat, Amsterdam", 
       "id": "000442"
     }, 
     {
       "lat": "4.92463546293141", 
       "lon": "52.3458880447308", 
       "name": "Fizeaustraat, Amsterdam", 
       "id": "000462"
     }, 
     {
       "lat": "4.93197386424648", 
       "lon": "52.3458266197262", 
       "name": "Lorentzlaan, Amsterdam", 
       "id": "000482"
     }, 
     {
       "lat": "4.93130758499424", 
       "lon": "52.3463992702597", 
       "name": "Lorentzlaan, Amsterdam", 
       "id": "000492"
     }, 
     {
       "lat": "4.93652647370453", 
       "lon": "52.3455114961604", 
       "name": "Maxwellstraat, Amsterdam", 
       "id": "000512"
     }, 
     {
       "lat": "4.93677321039505", 
       "lon": "52.3457820673918", 
       "name": "Maxwellstraat, Amsterdam", 
       "id": "000522"
     }, 
     {
       "lat": "4.93967712411697", 
       "lon": "52.3474198619835", 
       "name": "Kruislaan, Amsterdam", 
       "id": "000532"
     }, 
     {
       "lat": "4.93899037117381", 
       "lon": "52.3471206683478", 
       "name": "Kruislaan, Amsterdam", 
       "id": "000542"
     }, 
     {
       "lat": "4.94154331489566", 
       "lon": "52.3486492340183", 
       "name": "Linnaeusparkweg, Amsterdam", 
       "id": "000552"
     }, 
     {
       "lat": "4.93945568207298", 
       "lon": "52.3533688970743", 
       "name": "Radioweg, Amsterdam", 
       "id": "000592"
     }, 
     {
       "lat": "4.93979063601813", 
       "lon": "52.353630807356", 
       "name": "Radioweg, Amsterdam", 
       "id": "000602"
     }, 
     {
       "lat": "4.93965191821237", 
       "lon": "52.3557423960211", 
       "name": "Archimedesweg, Amsterdam", 
       "id": "000612"
     }, 
     {
       "lat": "4.93987390346488", 
       "lon": "52.3555634808038", 
       "name": "Archimedesweg, Amsterdam", 
       "id": "000622"
     }, 
     {
       "lat": "4.93487078018455", 
       "lon": "52.3510146581581", 
       "name": "Hugo de Vrieslaan, Amsterdam", 
       "id": "000651"
     }, 
     {
       "lat": "4.93487078018455", 
       "lon": "52.3510146581581", 
       "name": "Hugo de Vrieslaan, Amsterdam", 
       "id": "000652"
     }, 
     {
       "lat": "4.93540206740001", 
       "lon": "52.3507290800381", 
       "name": "Hugo de Vrieslaan, Amsterdam", 
       "id": "000661"
     }, 
     {
       "lat": "4.93540206740001", 
       "lon": "52.3507290800381", 
       "name": "Hugo de Vrieslaan, Amsterdam", 
       "id": "000662"
     }, 
     {
       "lat": "4.93993648344592", 
       "lon": "52.3478971918895", 
       "name": "Kruislaan, Amsterdam", 
       "id": "000701"
     }, 
     {
       "lat": "4.93993648344592", 
       "lon": "52.3478971918895", 
       "name": "Kruislaan, Amsterdam", 
       "id": "000702"
     }, 
     {
       "lat": "4.94045302519771", 
       "lon": "52.3476115353778", 
       "name": "Kruislaan, Amsterdam", 
       "id": "000711"
     }, 
     {
       "lat": "4.94045302519771", 
       "lon": "52.3476115353778", 
       "name": "Kruislaan, Amsterdam", 
       "id": "000712"
     }, 
     {
       "lat": "4.94797027990722", 
       "lon": "52.3428492109082", 
       "name": "Brinkstraat, Amsterdam", 
       "id": "000741"
     }, 
     {
       "lat": "4.94797027990722", 
       "lon": "52.3428492109082", 
       "name": "Brinkstraat, Amsterdam", 
       "id": "000742"
     }, 
     {
       "lat": "4.94742342550788", 
       "lon": "52.343242640385", 
       "name": "Brinkstraat, Amsterdam", 
       "id": "000761"
     }, 
     {
       "lat": "4.94742342550788", 
       "lon": "52.343242640385", 
       "name": "Brinkstraat, Amsterdam", 
       "id": "000762"
     }, 
     {
       "lat": "4.93840348522314", 
       "lon": "52.3398473662024", 
       "name": "Zaaiersweg, Amsterdam", 
       "id": "000792"
     }, 
     {
       "lat": "4.93948313114621", 
       "lon": "52.3390066077139", 
       "name": "Zaaiersweg, Amsterdam", 
       "id": "000802"
     }, 
     {
       "lat": "4.94902089479622", 
       "lon": "52.3211476877207", 
       "name": "Daalwijk, Amsterdam", 
       "id": "001112"
     }, 
     {
       "lat": "4.95004536083206", 
       "lon": "52.3213761716678", 
       "name": "Daalwijk, Amsterdam", 
       "id": "001122"
     }, 
     {
       "lat": "4.95124284235421", 
       "lon": "52.3219108684383", 
       "name": "Dennenrode, Amsterdam", 
       "id": "001132"
     }, 
     {
       "lat": "4.95213577325302", 
       "lon": "52.3220939105964", 
       "name": "Dennenrode, Amsterdam", 
       "id": "001142"
     }, 
     {
       "lat": "4.95399113718318", 
       "lon": "52.3228556907442", 
       "name": "Develstein, Amsterdam", 
       "id": "001152"
     }, 
     {
       "lat": "4.95505975810541", 
       "lon": "52.3230753049114", 
       "name": "Develstein, Amsterdam", 
       "id": "001162"
     }, 
     {
       "lat": "4.95951853897903", 
       "lon": "52.3246284128758", 
       "name": "Echtenstein, Amsterdam", 
       "id": "001182"
     }, 
     {
       "lat": "4.95972198794478", 
       "lon": "52.3248268787569", 
       "name": "Echtenstein, Amsterdam", 
       "id": "001192"
     }, 
     {
       "lat": "4.96270576725201", 
       "lon": "52.3257274088614", 
       "name": "Eeftink, Amsterdam", 
       "id": "001202"
     }, 
     {
       "lat": "4.96241222843491", 
       "lon": "52.3257443309134", 
       "name": "Eeftink, Amsterdam", 
       "id": "001212"
     }, 
     {
       "lat": "4.96486967615296", 
       "lon": "52.3264721479839", 
       "name": "Egeldonk, Amsterdam", 
       "id": "001222"
     }, 
     {
       "lat": "4.96459080182222", 
       "lon": "52.3264891277906", 
       "name": "Egeldonk, Amsterdam", 
       "id": "001232"
     }, 
     {
       "lat": "4.97091287530586", 
       "lon": "52.3249566578967", 
       "name": "Geldershoofd, Amsterdam", 
       "id": "001242"
     }, 
     {
       "lat": "4.97088151756864", 
       "lon": "52.3251722536071", 
       "name": "Geldershoofd, Amsterdam", 
       "id": "001252"
     }, 
     {
       "lat": "4.97626553666196", 
       "lon": "52.3235193531096", 
       "name": "Grubbehoeve, Amsterdam", 
       "id": "001262"
     }, 
     {
       "lat": "4.97765589676598", 
       "lon": "52.3238567205069", 
       "name": "Grubbehoeve, Amsterdam", 
       "id": "001272"
     }, 
     {
       "lat": "4.98077458789469", 
       "lon": "52.322869833832", 
       "name": "Geerdinkhof, Amsterdam", 
       "id": "001282"
     }, 
     {
       "lat": "4.98025414761996", 
       "lon": "52.3236409915066", 
       "name": "Geerdinkhof, Amsterdam", 
       "id": "001292"
     }, 
     {
       "lat": "4.98400667327901", 
       "lon": "52.3190700847764", 
       "name": "Koornhorst, Amsterdam", 
       "id": "001342"
     }, 
     {
       "lat": "4.98396047237268", 
       "lon": "52.31931259672", 
       "name": "Koornhorst, Amsterdam", 
       "id": "001352"
     }, 
     {
       "lat": "4.97868128603675", 
       "lon": "52.3160319291171", 
       "name": "Kraaienneststation, Amsterdam", 
       "id": "001412"
     }, 
     {
       "lat": "4.97236788314687", 
       "lon": "52.3168008835625", 
       "name": "Kikkenstein, Amsterdam", 
       "id": "001442"
     }, 
     {
       "lat": "4.97271063725439", 
       "lon": "52.316217880125", 
       "name": "Kikkenstein, Amsterdam", 
       "id": "001452"
     }, 
     {
       "lat": "4.96903340165601", 
       "lon": "52.3204831154929", 
       "name": "Gooioord, Amsterdam", 
       "id": "001462"
     }, 
     {
       "lat": "4.9693611390031", 
       "lon": "52.3199450077333", 
       "name": "Gooioord, Amsterdam", 
       "id": "001472"
     }, 
     {
       "lat": "4.96535711512276", 
       "lon": "52.3199397869739", 
       "name": "Geinwijk, Amsterdam", 
       "id": "001502"
     }, 
     {
       "lat": "4.96584196001241", 
       "lon": "52.3198516370573", 
       "name": "Geinwijk, Amsterdam", 
       "id": "001512"
     }, 
     {
       "lat": "4.95858901462317", 
       "lon": "52.3175876295797", 
       "name": "Florijn, Amsterdam", 
       "id": "001522"
     }, 
     {
       "lat": "4.95971645404205", 
       "lon": "52.3177804519261", 
       "name": "Florijn, Amsterdam", 
       "id": "001532"
     }, 
     {
       "lat": "4.95148948668799", 
       "lon": "52.316204541776", 
       "name": "Frissenstein, Amsterdam", 
       "id": "001542"
     }, 
     {
       "lat": "4.95131465066402", 
       "lon": "52.316087056628", 
       "name": "Frissenstein, Amsterdam", 
       "id": "001552"
     }, 
     {
       "lat": "4.94843588786909", 
       "lon": "52.3194917697346", 
       "name": "Dolingadreef, Amsterdam", 
       "id": "001562"
     }, 
     {
       "lat": "4.94846761671564", 
       "lon": "52.3192492175279", 
       "name": "Dolingadreef, Amsterdam", 
       "id": "001572"
     }, 
     {
       "lat": "4.95860831872665", 
       "lon": "52.3125455575759", 
       "name": "Hofgeest, Amsterdam", 
       "id": "001642"
     }, 
     {
       "lat": "4.95956172925274", 
       "lon": "52.3094751865243", 
       "name": "Hogevecht, Amsterdam", 
       "id": "001672"
     }, 
     {
       "lat": "4.9599725517745", 
       "lon": "52.3094497076201", 
       "name": "Hogevecht, Amsterdam", 
       "id": "001682"
     }, 
     {
       "lat": "4.96076176007413", 
       "lon": "52.3066663415329", 
       "name": "Huigenbos, Amsterdam", 
       "id": "001692"
     }, 
     {
       "lat": "4.96083291487687", 
       "lon": "52.3068912927461", 
       "name": "Huigenbos, Amsterdam", 
       "id": "001702"
     }, 
     {
       "lat": "4.96483635795469", 
       "lon": "52.302205040987", 
       "name": "Maasdrielhof, Amsterdam", 
       "id": "001712"
     }, 
     {
       "lat": "4.96402620157752", 
       "lon": "52.2995237816699", 
       "name": "Holendrechtplein, Amsterdam", 
       "id": "001722"
     }, 
     {
       "lat": "4.96309192512433", 
       "lon": "52.2991069964111", 
       "name": "Holendrechtplein, Amsterdam", 
       "id": "001732"
     }, 
     {
       "lat": "4.96548526065232", 
       "lon": "52.3018029056232", 
       "name": "Maasdrielhof, Amsterdam", 
       "id": "001742"
     }, 
     {
       "lat": "4.97179735398325", 
       "lon": "52.3135093584264", 
       "name": "Kelbergen, Amsterdam", 
       "id": "001792"
     }, 
     {
       "lat": "4.97143040948922", 
       "lon": "52.3135440204569", 
       "name": "Kelbergen, Amsterdam", 
       "id": "001802"
     }, 
     {
       "lat": "4.96784069192326", 
       "lon": "52.2992227950973", 
       "name": "Meernhof, Amsterdam", 
       "id": "001842"
     }, 
     {
       "lat": "4.96710304050719", 
       "lon": "52.2997145062267", 
       "name": "Meernhof, Amsterdam", 
       "id": "001852"
     }, 
     {
       "lat": "5.013125871486", 
       "lon": "52.3044258155534", 
       "name": "Geinbrug, Amsterdam", 
       "id": "001862"
     }, 
     {
       "lat": "5.01277354397517", 
       "lon": "52.3044786274491", 
       "name": "Geinbrug, Amsterdam", 
       "id": "001872"
     }, 
     {
       "lat": "4.95873784402054", 
       "lon": "52.297590339927", 
       "name": "Station Holendrecht , Amsterdam", 
       "id": "001902"
     }, 
     {
       "lat": "4.95980302997126", 
       "lon": "52.298106498885", 
       "name": "Station Holendrecht , Amsterdam", 
       "id": "001922"
     }, 
     {
       "lat": "4.9729167063575", 
       "lon": "52.3224291445188", 
       "name": "Station Ganzenhoef, Amsterdam", 
       "id": "001952"
     }, 
     {
       "lat": "4.9741744989738", 
       "lon": "52.3228200153346", 
       "name": "Station Ganzenhoef, Amsterdam", 
       "id": "001962"
     }, 
     {
       "lat": "4.97161779300142", 
       "lon": "52.3217325320846", 
       "name": "Annie Romeinplein, Amsterdam", 
       "id": "001972"
     }, 
     {
       "lat": "4.96997787005792", 
       "lon": "52.3214301645464", 
       "name": "Annie Romeinplein, Amsterdam", 
       "id": "001982"
     }, 
     {
       "lat": "4.97329194270371", 
       "lon": "52.3230865638616", 
       "name": "Station Ganzenhoef, Amsterdam", 
       "id": "001992"
     }, 
     {
       "lat": "4.97508246070616", 
       "lon": "52.3229759731435", 
       "name": "Station Ganzenhoef, Amsterdam", 
       "id": "002002"
     }, 
     {
       "lat": "5.00096200374881", 
       "lon": "52.3105523321004", 
       "name": "Reigersbroeck, Amsterdam", 
       "id": "002012"
     }, 
     {
       "lat": "4.99981144352031", 
       "lon": "52.311330505346", 
       "name": "Reigersbroeck, Amsterdam", 
       "id": "002022"
     }, 
     {
       "lat": "4.95866818732894", 
       "lon": "52.2972125997124", 
       "name": "Station Holendrecht , Amsterdam", 
       "id": "002052"
     }, 
     {
       "lat": "4.97003576872277", 
       "lon": "52.2980801195751", 
       "name": "Rhenenhof, Amsterdam", 
       "id": "002062"
     }, 
     {
       "lat": "4.97082458948377", 
       "lon": "52.2983794965805", 
       "name": "Rhenenhof, Amsterdam", 
       "id": "002072"
     }, 
     {
       "lat": "4.95576366603952", 
       "lon": "52.3079873979684", 
       "name": "Hakfort, Amsterdam", 
       "id": "002092"
     }, 
     {
       "lat": "4.95541115534441", 
       "lon": "52.3080490262543", 
       "name": "Hakfort, Amsterdam", 
       "id": "002102"
     }, 
     {
       "lat": "4.95872699628049", 
       "lon": "52.2971948371713", 
       "name": "Station Holendrecht , Amsterdam", 
       "id": "002112"
     }, 
     {
       "lat": "4.9850595890862", 
       "lon": "52.3113082419479", 
       "name": "Gaasperplas, Amsterdam", 
       "id": "002192"
     }, 
     {
       "lat": "4.99294709187663", 
       "lon": "52.3148130551928", 
       "name": "Gaasp, Amsterdam", 
       "id": "002202"
     }, 
     {
       "lat": "4.99214444387847", 
       "lon": "52.3143699774461", 
       "name": "Gaasp, Amsterdam", 
       "id": "002212"
     }, 
     {
       "lat": "4.95264849001488", 
       "lon": "52.2936674124882", 
       "name": "Meibergdreef, Amsterdam", 
       "id": "002282"
     }, 
     {
       "lat": "4.95593957278691", 
       "lon": "52.2913695910976", 
       "name": "A.Z.U.A., Amsterdam", 
       "id": "002312"
     }, 
     {
       "lat": "4.97374636237237", 
       "lon": "52.2963225528625", 
       "name": "Station Reigersbos, Amsterdam", 
       "id": "002352"
     }, 
     {
       "lat": "4.95761818593149", 
       "lon": "52.3133328907948", 
       "name": "Hofgeest, Amsterdam", 
       "id": "002362"
     }, 
     {
       "lat": "4.95375239693169", 
       "lon": "52.3157544777639", 
       "name": "Flierbosdreef, Amsterdam", 
       "id": "002372"
     }, 
     {
       "lat": "4.95413097245527", 
       "lon": "52.3160344852659", 
       "name": "Flierbosdreef, Amsterdam", 
       "id": "002382"
     }, 
     {
       "lat": "4.95597406928716", 
       "lon": "52.3165265576426", 
       "name": "Anton de Komplein, Amsterdam", 
       "id": "002392"
     }, 
     {
       "lat": "4.9566862768669", 
       "lon": "52.3308107040928", 
       "name": "Station Diemen Zuid, Diemen", 
       "id": "002502"
     }, 
     {
       "lat": "4.95681717482509", 
       "lon": "52.3309280209806", 
       "name": "Station Diemen Zuid, Diemen", 
       "id": "002512"
     }, 
     {
       "lat": "4.95487615105538", 
       "lon": "52.332898249915", 
       "name": "Tarwekamp, Diemen", 
       "id": "002522"
     }, 
     {
       "lat": "4.95472725601409", 
       "lon": "52.3331223994994", 
       "name": "Tarwekamp, Diemen", 
       "id": "002532"
     }, 
     {
       "lat": "4.94572930453038", 
       "lon": "52.3306175413754", 
       "name": "Biesbosch, Diemen", 
       "id": "002542"
     }, 
     {
       "lat": "4.94433915591103", 
       "lon": "52.3302618243375", 
       "name": "Biesbosch, Diemen", 
       "id": "002552"
     }, 
     {
       "lat": "4.9392866962061", 
       "lon": "52.327932952588", 
       "name": "Kruidenommegang, Duivendrecht", 
       "id": "002562"
     }, 
     {
       "lat": "4.93938865457619", 
       "lon": "52.3280052406043", 
       "name": "Kruidenommegang, Duivendrecht", 
       "id": "002572"
     }, 
     {
       "lat": "4.93685281396916", 
       "lon": "52.3321479616354", 
       "name": "Lunaweg, Duivendrecht", 
       "id": "002602"
     }, 
     {
       "lat": "4.93694001645885", 
       "lon": "52.3322291832856", 
       "name": "Lunaweg, Duivendrecht", 
       "id": "002612"
     }, 
     {
       "lat": "4.94027098752891", 
       "lon": "52.3292488876105", 
       "name": "Rijksstraatweg, Duivendrecht", 
       "id": "002642"
     }, 
     {
       "lat": "4.93927319144367", 
       "lon": "52.32927207796", 
       "name": "Rijksstraatweg, Duivendrecht", 
       "id": "002652"
     }, 
     {
       "lat": "4.9399437339265", 
       "lon": "52.3296970390961", 
       "name": "Korenbloemstraat, Duivendrecht", 
       "id": "002662"
     }, 
     {
       "lat": "4.9400871730275", 
       "lon": "52.3300211405045", 
       "name": "Korenbloemstraat, Duivendrecht", 
       "id": "002672"
     }, 
     {
       "lat": "4.93423523763813", 
       "lon": "52.3298730552112", 
       "name": "Astronautenweg, Duivendrecht", 
       "id": "002682"
     }, 
     {
       "lat": "4.93485099770799", 
       "lon": "52.3299113618088", 
       "name": "Astronautenweg, Duivendrecht", 
       "id": "002692"
     }, 
     {
       "lat": "4.94119726115386", 
       "lon": "52.3085894817614", 
       "name": "Holterbergweg, Amsterdam", 
       "id": "002762"
     }, 
     {
       "lat": "4.93304877578071", 
       "lon": "52.361253677881", 
       "name": "Muiderpoortstation, Amsterdam", 
       "id": "002772"
     }, 
     {
       "lat": "4.93755862821745", 
       "lon": "52.307353365842", 
       "name": "Keienbergweg, Amsterdam", 
       "id": "002822"
     }, 
     {
       "lat": "4.94054635397637", 
       "lon": "52.301864149985", 
       "name": "Klokkenbergweg, Amsterdam", 
       "id": "002882"
     }, 
     {
       "lat": "4.93706247201291", 
       "lon": "52.3056707598846", 
       "name": "Kollenbergweg, Amsterdam", 
       "id": "002942"
     }, 
     {
       "lat": "4.94233975379284", 
       "lon": "52.3248257162784", 
       "name": "Dalsteindreef, Amsterdam", 
       "id": "002952"
     }, 
     {
       "lat": "4.94241327386", 
       "lon": "52.3248080171446", 
       "name": "Dalsteindreef, Amsterdam", 
       "id": "002962"
     }, 
     {
       "lat": "4.98510447445233", 
       "lon": "52.3112095290646", 
       "name": "Gaasperplas, Amsterdam", 
       "id": "003042"
     }, 
     {
       "lat": "4.97848918384508", 
       "lon": "52.3098117294237", 
       "name": "Leusdenhof, Amsterdam", 
       "id": "003052"
     }, 
     {
       "lat": "4.97837105214762", 
       "lon": "52.3099011989635", 
       "name": "Leusdenhof, Amsterdam", 
       "id": "003062"
     }, 
     {
       "lat": "4.97402449841533", 
       "lon": "52.3074054704594", 
       "name": "Leerdamhof, Amsterdam", 
       "id": "003072"
     }, 
     {
       "lat": "4.97526021328311", 
       "lon": "52.3053875292816", 
       "name": "Leerdamhof, Amsterdam", 
       "id": "003142"
     }, 
     {
       "lat": "4.98507474065551", 
       "lon": "52.3112543668402", 
       "name": "Gaasperplas, Amsterdam", 
       "id": "003152"
     }, 
     {
       "lat": "4.98513648493063", 
       "lon": "52.3109130414833", 
       "name": "Gaasperplas, Amsterdam", 
       "id": "003212"
     }, 
     {
       "lat": "4.9851636979456", 
       "lon": "52.3111468159674", 
       "name": "Gaasperplas, Amsterdam", 
       "id": "003222"
     }, 
     {
       "lat": "4.98519351288099", 
       "lon": "52.3110929906756", 
       "name": "Gaasperplas, Amsterdam", 
       "id": "003232"
     }, 
     {
       "lat": "4.95878153928396", 
       "lon": "52.2960985222963", 
       "name": "Academisch Medisch Centrum, Amsterdam", 
       "id": "003252"
     }, 
     {
       "lat": "4.93455366776935", 
       "lon": "52.3504472192556", 
       "name": "Middenweg, Amsterdam", 
       "id": "003302"
     }, 
     {
       "lat": "4.97347272113967", 
       "lon": "52.297373168456", 
       "name": "Station Reigersbos, Amsterdam", 
       "id": "003312"
     }, 
     {
       "lat": "4.97448791350336", 
       "lon": "52.293817546172", 
       "name": "Schoonhovendreef, Amsterdam", 
       "id": "003322"
     }, 
     {
       "lat": "4.97463257374165", 
       "lon": "52.2940247703965", 
       "name": "Schoonhovendreef, Amsterdam", 
       "id": "003332"
     }, 
     {
       "lat": "4.97739993959426", 
       "lon": "52.2927671116872", 
       "name": "Scherpenzeelstraat, Amsterdam", 
       "id": "003342"
     }, 
     {
       "lat": "4.97723771281631", 
       "lon": "52.2928744030872", 
       "name": "Scherpenzeelstraat, Amsterdam", 
       "id": "003352"
     }, 
     {
       "lat": "4.98157847368939", 
       "lon": "52.2926556878849", 
       "name": "Schaarsbergenstraat, Amsterdam", 
       "id": "003362"
     }, 
     {
       "lat": "4.98129907947738", 
       "lon": "52.2927535951124", 
       "name": "Schaarsbergenstraat, Amsterdam", 
       "id": "003372"
     }, 
     {
       "lat": "4.98601830717164", 
       "lon": "52.2928236249315", 
       "name": "Wageningendreef, Amsterdam", 
       "id": "003382"
     }, 
     {
       "lat": "4.98584176790815", 
       "lon": "52.2928949283356", 
       "name": "Wageningendreef, Amsterdam", 
       "id": "003392"
     }, 
     {
       "lat": "4.98905314992357", 
       "lon": "52.2943887698632", 
       "name": "Gein, Amsterdam", 
       "id": "003402"
     }, 
     {
       "lat": "4.9888204733835", 
       "lon": "52.294181267015", 
       "name": "Gein, Amsterdam", 
       "id": "003412"
     }, 
     {
       "lat": "4.9892918382598", 
       "lon": "52.2988385302433", 
       "name": "Gein, Amsterdam", 
       "id": "003422"
     }, 
     {
       "lat": "4.98914709401083", 
       "lon": "52.2986313240652", 
       "name": "Gein, Amsterdam", 
       "id": "003432"
     }, 
     {
       "lat": "4.98910978297274", 
       "lon": "52.296249433943", 
       "name": "Station Gein, Amsterdam", 
       "id": "003452"
     }, 
     {
       "lat": "4.98935729123887", 
       "lon": "52.2964390104186", 
       "name": "Station Gein, Amsterdam", 
       "id": "003462"
     }, 
     {
       "lat": "4.9510403629475", 
       "lon": "52.3111607413285", 
       "name": "Haardstee, Amsterdam", 
       "id": "003472"
     }, 
     {
       "lat": "4.95136410624357", 
       "lon": "52.3110450933297", 
       "name": "Haardstee, Amsterdam", 
       "id": "003482"
     }, 
     {
       "lat": "4.94525009862789", 
       "lon": "52.3227514609111", 
       "name": "Dostojevskisingel, Amsterdam", 
       "id": "003512"
     }, 
     {
       "lat": "4.94457146102336", 
       "lon": "52.3231443858508", 
       "name": "Dostojevskisingel, Amsterdam", 
       "id": "003522"
     }, 
     {
       "lat": "4.93706338224762", 
       "lon": "52.3055808853185", 
       "name": "Kollenbergweg, Amsterdam", 
       "id": "003552"
     }, 
     {
       "lat": "4.93881295153273", 
       "lon": "52.303655152719", 
       "name": "Kuiperbergweg, Amsterdam", 
       "id": "003562"
     }, 
     {
       "lat": "4.94032500181834", 
       "lon": "52.302007118793", 
       "name": "Klokkenbergweg, Amsterdam", 
       "id": "003572"
     }, 
     {
       "lat": "4.93741173294701", 
       "lon": "52.3073797707564", 
       "name": "Keienbergweg, Amsterdam", 
       "id": "003582"
     }, 
     {
       "lat": "4.94343822860645", 
       "lon": "52.3014975475273", 
       "name": "Luttenbergweg, Amsterdam", 
       "id": "003592"
     }, 
     {
       "lat": "4.95497672240544", 
       "lon": "52.3346242642079", 
       "name": "Bovenrijkersloot, Diemen", 
       "id": "003642"
     }, 
     {
       "lat": "4.95544244586354", 
       "lon": "52.3350124372182", 
       "name": "Bovenrijkersloot, Diemen", 
       "id": "003652"
     }, 
     {
       "lat": "4.95524879024475", 
       "lon": "52.3307874900298", 
       "name": "Station Diemen Zuid, Diemen", 
       "id": "003662"
     }, 
     {
       "lat": "4.95466251517382", 
       "lon": "52.3307314219806", 
       "name": "Station Diemen Zuid, Diemen", 
       "id": "003672"
     }, 
     {
       "lat": "4.94100174725245", 
       "lon": "52.3324422991406", 
       "name": "Plataanstraat, Duivendrecht", 
       "id": "003702"
     }, 
     {
       "lat": "4.9410316300636", 
       "lon": "52.332388485291", 
       "name": "Plataanstraat, Duivendrecht", 
       "id": "003712"
     }, 
     {
       "lat": "4.94244420469459", 
       "lon": "52.301206204001", 
       "name": "Luttenbergweg, Amsterdam", 
       "id": "003742"
     }, 
     {
       "lat": "4.93829309885013", 
       "lon": "52.3043182784394", 
       "name": "Kuiperbergweg, Amsterdam", 
       "id": "003862"
     }, 
     {
       "lat": "4.95937869322094", 
       "lon": "52.2919303395163", 
       "name": "A.Z.U.A., Amsterdam", 
       "id": "004032"
     }, 
     {
       "lat": "4.96090728082471", 
       "lon": "52.2945513127784", 
       "name": "Faculteit, Amsterdam", 
       "id": "004042"
     }, 
     {
       "lat": "4.98591079782654", 
       "lon": "52.3014874924023", 
       "name": "Wamelstraat, Amsterdam", 
       "id": "004192"
     }, 
     {
       "lat": "4.98555813669925", 
       "lon": "52.3015761732595", 
       "name": "Wamelstraat, Amsterdam", 
       "id": "004202"
     }, 
     {
       "lat": "4.98085296929262", 
       "lon": "52.3014702245581", 
       "name": "Veenendaalplein, Amsterdam", 
       "id": "004212"
     }, 
     {
       "lat": "4.98041233588299", 
       "lon": "52.301558587832", 
       "name": "Veenendaalplein, Amsterdam", 
       "id": "004222"
     }, 
     {
       "lat": "4.95031760172954", 
       "lon": "52.3145734319517", 
       "name": "Bijlmerplein, Amsterdam", 
       "id": "004342"
     }, 
     {
       "lat": "4.95113458823008", 
       "lon": "52.3150078596612", 
       "name": "Bijlmerplein, Amsterdam", 
       "id": "004352"
     }, 
     {
       "lat": "4.94579816144131", 
       "lon": "52.3354981467016", 
       "name": "Industrieweg, Duivendrecht", 
       "id": "004362"
     }, 
     {
       "lat": "4.94539961543187", 
       "lon": "52.3357393286182", 
       "name": "Industrieweg, Duivendrecht", 
       "id": "004372"
     }, 
     {
       "lat": "4.93253874983419", 
       "lon": "52.3608832242414", 
       "name": "Muiderpoortstation, Amsterdam", 
       "id": "004411"
     }, 
     {
       "lat": "4.96005397363657", 
       "lon": "52.337590677349", 
       "name": "Beukenhorst, Diemen", 
       "id": "004422"
     }, 
     {
       "lat": "4.96005604851452", 
       "lon": "52.3373749791946", 
       "name": "Beukenhorst, Diemen", 
       "id": "004432"
     }, 
     {
       "lat": "4.92490034783607", 
       "lon": "52.3599099327384", 
       "name": "Linnaeusstraat, Amsterdam", 
       "id": "004441"
     }, 
     {
       "lat": "4.92490034783607", 
       "lon": "52.3599099327384", 
       "name": "Linnaeusstraat, Amsterdam", 
       "id": "004442"
     }, 
     {
       "lat": "4.95832525341906", 
       "lon": "52.3388337203502", 
       "name": "Schoolstraat, Diemen", 
       "id": "004451"
     }, 
     {
       "lat": "4.95832525341906", 
       "lon": "52.3388337203502", 
       "name": "Schoolstraat, Diemen", 
       "id": "004452"
     }, 
     {
       "lat": "4.95895773851919", 
       "lon": "52.3386742314924", 
       "name": "Schoolstraat, Diemen", 
       "id": "004461"
     }, 
     {
       "lat": "4.96546855340989", 
       "lon": "52.3375561699599", 
       "name": "Nic. Lublinkstraat, Diemen", 
       "id": "004471"
     }, 
     {
       "lat": "4.96546855340989", 
       "lon": "52.3375561699599", 
       "name": "Nic. Lublinkstraat, Diemen", 
       "id": "004472"
     }, 
     {
       "lat": "4.96605672239672", 
       "lon": "52.3374234484837", 
       "name": "Nic. Lublinkstraat, Diemen", 
       "id": "004481"
     }, 
     {
       "lat": "4.96605672239672", 
       "lon": "52.3374234484837", 
       "name": "Nic. Lublinkstraat, Diemen", 
       "id": "004482"
     }, 
     {
       "lat": "4.97020374162299", 
       "lon": "52.336431507429", 
       "name": "Diemen (Sniep), Diemen", 
       "id": "004491"
     }, 
     {
       "lat": "4.96943792840251", 
       "lon": "52.3367343894326", 
       "name": "Diemen (Sniep), Diemen", 
       "id": "004501"
     }, 
     {
       "lat": "4.9557412870822", 
       "lon": "52.2966986410135", 
       "name": "Paasheuvelweg, Amsterdam", 
       "id": "004522"
     }, 
     {
       "lat": "4.96043501282236", 
       "lon": "52.3269505629408", 
       "name": "Hogeschool InHolland, Diemen", 
       "id": "004602"
     }, 
     {
       "lat": "4.96043691250509", 
       "lon": "52.3267528392106", 
       "name": "Hogeschool InHolland, Diemen", 
       "id": "004612"
     }, 
     {
       "lat": "4.95149855759285", 
       "lon": "52.3541598161819", 
       "name": "Science Park A'dam, Amsterdam", 
       "id": "004792"
     }, 
     {
       "lat": "4.93322686726424", 
       "lon": "52.361065619087", 
       "name": "Muiderpoortstation, Amsterdam", 
       "id": "004852"
     }, 
     {
       "lat": "4.9529108648345", 
       "lon": "52.3553334080188", 
       "name": "Science Park A'dam, Amsterdam", 
       "id": "004922"
     }, 
     {
       "lat": "4.95444251523814", 
       "lon": "52.3563186770809", 
       "name": "Science Park Aqua, Amsterdam", 
       "id": "004972"
     }, 
     {
       "lat": "4.9601227314025", 
       "lon": "52.3563752564738", 
       "name": "Science Park Ignis, Amsterdam", 
       "id": "004992"
     }, 
     {
       "lat": "4.95973645417907", 
       "lon": "52.3553312888008", 
       "name": "Science Park Aer, Amsterdam", 
       "id": "005012"
     }, 
     {
       "lat": "4.95677335578622", 
       "lon": "52.3536128877874", 
       "name": "Science Park Terra, Amsterdam", 
       "id": "005032"
     }, 
     {
       "lat": "4.95435539835458", 
       "lon": "52.339664114641", 
       "name": "Arent Krijtsstraat, Diemen", 
       "id": "005041"
     }, 
     {
       "lat": "4.95435539835458", 
       "lon": "52.339664114641", 
       "name": "Arent Krijtsstraat, Diemen", 
       "id": "005042"
     }, 
     {
       "lat": "4.9546938389516", 
       "lon": "52.3395664868825", 
       "name": "Arent Krijtsstraat, Diemen", 
       "id": "005051"
     }, 
     {
       "lat": "4.9546938389516", 
       "lon": "52.3395664868825", 
       "name": "Arent Krijtsstraat, Diemen", 
       "id": "005052"
     }, 
     {
       "lat": "4.93618514540197", 
       "lon": "52.3227711794698", 
       "name": "Station Duivendrecht, Duivendrecht", 
       "id": "005092"
     }, 
     {
       "lat": "4.9366514007315", 
       "lon": "52.323078540194", 
       "name": "Station Duivendrecht, Duivendrecht", 
       "id": "005112"
     }, 
     {
       "lat": "4.93389570471572", 
       "lon": "52.3502020327128", 
       "name": "Middenweg, Amsterdam", 
       "id": "005122"
     }, 
     {
       "lat": "4.9361097097327", 
       "lon": "52.322977610676", 
       "name": "Station Duivendrecht, Duivendrecht", 
       "id": "005152"
     }, 
     {
       "lat": "4.94937777180785", 
       "lon": "52.3132128023499", 
       "name": "Foppingadreef, Amsterdam", 
       "id": "005172"
     }, 
     {
       "lat": "4.94967627667792", 
       "lon": "52.3126836275072", 
       "name": "Foppingadreef, Amsterdam", 
       "id": "005182"
     }, 
     {
       "lat": "4.97189976712265", 
       "lon": "52.3276564505628", 
       "name": "Provincialeweg, Diemen", 
       "id": "005252"
     }, 
     {
       "lat": "4.97351973951392", 
       "lon": "52.3285519118915", 
       "name": "Provincialeweg, Diemen", 
       "id": "005262"
     }, 
     {
       "lat": "4.96666676642051", 
       "lon": "52.3272335196225", 
       "name": "Eekholt, Amsterdam", 
       "id": "005272"
     }, 
     {
       "lat": "4.96706316542647", 
       "lon": "52.3271989767623", 
       "name": "Eekholt, Amsterdam", 
       "id": "005282"
     }, 
     {
       "lat": "4.94781801098861", 
       "lon": "52.3523037308448", 
       "name": "Archimedesplantsoen, Amsterdam", 
       "id": "005292"
     }, 
     {
       "lat": "4.94275547483196", 
       "lon": "52.3492469815094", 
       "name": "Linnaeusparkweg, Amsterdam", 
       "id": "005372"
     }, 
     {
       "lat": "4.94808130978532", 
       "lon": "52.3523945850328", 
       "name": "Archimedesplantsoen, Amsterdam", 
       "id": "005382"
     }, 
     {
       "lat": "4.92197544864605", 
       "lon": "52.3378425725305", 
       "name": "Station Spaklerweg, Amsterdam", 
       "id": "005482"
     }, 
     {
       "lat": "4.9217563064744", 
       "lon": "52.3377518332884", 
       "name": "Station Spaklerweg, Amsterdam", 
       "id": "005492"
     }, 
     {
       "lat": "4.91570766868504", 
       "lon": "52.3297827043183", 
       "name": "Joan Muyskenweg, Duivendrecht", 
       "id": "005502"
     }, 
     {
       "lat": "4.91566404153367", 
       "lon": "52.3297465793793", 
       "name": "Joan Muyskenweg, Duivendrecht", 
       "id": "005512"
     }, 
     {
       "lat": "4.98156285874109", 
       "lon": "52.3168597304853", 
       "name": "Kraaienneststation, Amsterdam", 
       "id": "005522"
     }, 
     {
       "lat": "4.98073465669054", 
       "lon": "52.3160120383734", 
       "name": "Kraaienneststation, Amsterdam", 
       "id": "005532"
     }, 
     {
       "lat": "4.95087900063667", 
       "lon": "52.3544721040241", 
       "name": "Science Park A'dam, Amsterdam", 
       "id": "005542"
     }, 
     {
       "lat": "4.95033211689326", 
       "lon": "52.3548565585207", 
       "name": "Science Park A'dam, Amsterdam", 
       "id": "005552"
     }, 
     {
       "lat": "4.94469727190946", 
       "lon": "52.3576308067726", 
       "name": "C. Mac Gillavrylaan, Amsterdam", 
       "id": "005562"
     }, 
     {
       "lat": "4.94415343609491", 
       "lon": "52.3577006743599", 
       "name": "C. Mac Gillavrylaan, Amsterdam", 
       "id": "005572"
     }, 
     {
       "lat": "4.94753516081029", 
       "lon": "52.3112106799927", 
       "name": "Station Bijlmer ArenA, Amsterdam", 
       "id": "005592"
     }, 
     {
       "lat": "4.94747606203549", 
       "lon": "52.3112553992642", 
       "name": "Station Bijlmer ArenA, Amsterdam", 
       "id": "005602"
     }, 
     {
       "lat": "4.94731316168958", 
       "lon": "52.3114165737967", 
       "name": "Station Bijlmer ArenA, Amsterdam", 
       "id": "005632"
     }, 
     {
       "lat": "4.94728330066888", 
       "lon": "52.3114703894776", 
       "name": "Station Bijlmer ArenA, Amsterdam", 
       "id": "005642"
     }, 
     {
       "lat": "4.93140369610354", 
       "lon": "52.3241729244514", 
       "name": "Stationsweg, Amsterdam", 
       "id": "005702"
     }, 
     {
       "lat": "4.93110960222735", 
       "lon": "52.3242436933307", 
       "name": "Stationsweg, Amsterdam", 
       "id": "005712"
     }, 
     {
       "lat": "4.91937210057489", 
       "lon": "52.3412206926259", 
       "name": "H.J.E. Wenckebachweg, Amsterdam", 
       "id": "005732"
     }, 
     {
       "lat": "4.91956219209676", 
       "lon": "52.3412843581521", 
       "name": "H.J.E. Wenckebachweg, Amsterdam", 
       "id": "005742"
     }, 
     {
       "lat": "5.02488995347337", 
       "lon": "52.3325491134961", 
       "name": "Maxisweg, Muiden", 
       "id": "009632"
     }, 
     {
       "lat": "5.02596113318183", 
       "lon": "52.3325254249131", 
       "name": "Maxisweg, Muiden", 
       "id": "009642"
     }, 
     {
       "lat": "4.97931644139786", 
       "lon": "52.3506818303878", 
       "name": "Tureluurweg, Diemen", 
       "id": "009662"
     }, 
     {
       "lat": "4.97159546501314", 
       "lon": "52.3476351037341", 
       "name": "Landlust, Diemen", 
       "id": "009672"
     }, 
     {
       "lat": "4.98591061277579", 
       "lon": "52.3469744722327", 
       "name": "Diemen Noord, Diemen", 
       "id": "009702"
     }, 
     {
       "lat": "4.97382571410192", 
       "lon": "52.3508425373238", 
       "name": "Rietzangerweg, Diemen", 
       "id": "009712"
     }, 
     {
       "lat": "4.9710623730684", 
       "lon": "52.3512732525891", 
       "name": "Oude Waelweg, Diemen", 
       "id": "009722"
     }, 
     {
       "lat": "4.9735626025909", 
       "lon": "52.3491519294683", 
       "name": "Vogelweg, Diemen", 
       "id": "009732"
     }, 
     {
       "lat": "4.97046594512821", 
       "lon": "52.3491410677421", 
       "name": "Buytenweg, Diemen", 
       "id": "009742"
     }, 
     {
       "lat": "4.96742357044171", 
       "lon": "52.3449420425792", 
       "name": "Station Diemen, Diemen", 
       "id": "009752"
     }, 
     {
       "lat": "4.98288562125227", 
       "lon": "52.3487796945955", 
       "name": "Klipperweg, Diemen", 
       "id": "009762"
     }, 
     {
       "lat": "4.98256078316848", 
       "lon": "52.3489942894859", 
       "name": "Klipperweg, Diemen", 
       "id": "009772"
     }, 
     {
       "lat": "4.97903593277253", 
       "lon": "52.3508606175277", 
       "name": "Tureluurweg, Diemen", 
       "id": "009782"
     }, 
     {
       "lat": "4.97635254939552", 
       "lon": "52.352172526643", 
       "name": "Meerkoet, Diemen", 
       "id": "009792"
     }, 
     {
       "lat": "4.97580533137145", 
       "lon": "52.3526200111625", 
       "name": "Zeezigt, Diemen", 
       "id": "009802"
     }, 
     {
       "lat": "4.96422433521757", 
       "lon": "52.3418658395381", 
       "name": "Winkelcentrum, Diemen", 
       "id": "009852"
     }, 
     {
       "lat": "4.9681343251437", 
       "lon": "52.3380509769685", 
       "name": "Prins Bernhardlaan, Diemen", 
       "id": "009862"
     }, 
     {
       "lat": "4.96812185634754", 
       "lon": "52.3393721289601", 
       "name": "Prins Bernhardlaan, Diemen", 
       "id": "009872"
     }, 
     {
       "lat": "4.9656352237122", 
       "lon": "52.3431830809908", 
       "name": "De Diem, Diemen", 
       "id": "009892"
     }, 
     {
       "lat": "4.96526939566561", 
       "lon": "52.3430739247431", 
       "name": "De Diem, Diemen", 
       "id": "009902"
     }, 
     {
       "lat": "4.96784395829278", 
       "lon": "52.345491783544", 
       "name": "Station Diemen, Diemen", 
       "id": "009912"
     }, 
     {
       "lat": "4.9677061763641", 
       "lon": "52.3398829567659", 
       "name": "Pr. Beatrixlaan, Diemen", 
       "id": "009922"
     }, 
     {
       "lat": "4.962588446746", 
       "lon": "52.3410690619044", 
       "name": "Burg. Bickerstraat, Diemen", 
       "id": "009932"
     }, 
     {
       "lat": "4.96277842796417", 
       "lon": "52.3411506328915", 
       "name": "Burg. Bickerstraat, Diemen", 
       "id": "009942"
     }, 
     {
       "lat": "4.95729923185834", 
       "lon": "52.3417510105042", 
       "name": "Wilhelminaplantsoen, Diemen", 
       "id": "009952"
     }, 
     {
       "lat": "4.95740099027791", 
       "lon": "52.3418502451008", 
       "name": "Wilhelminaplantsoen, Diemen", 
       "id": "009962"
     }, 
     {
       "lat": "4.98070737361058", 
       "lon": "52.3334212112613", 
       "name": "Vinkenbrug, Diemen", 
       "id": "009982"
     }, 
     {
       "lat": "4.98085548071383", 
       "lon": "52.3332689284643", 
       "name": "Vinkenbrug, Diemen", 
       "id": "009992"
     }, 
     {
       "lat": "4.95884155709221", 
       "lon": "52.3902541482296", 
       "name": "Hilversumstraat, Amsterdam", 
       "id": "010012"
     }, 
     {
       "lat": "4.95897879902368", 
       "lon": "52.3897333613282", 
       "name": "Hilversumstraat, Amsterdam", 
       "id": "010022"
     }, 
     {
       "lat": "4.95756430891368", 
       "lon": "52.3916875444859", 
       "name": "Volendammerweg, Amsterdam", 
       "id": "010042"
     }, 
     {
       "lat": "4.95680176115899", 
       "lon": "52.3930598846238", 
       "name": "Volendammerweg, Amsterdam", 
       "id": "010052"
     }, 
     {
       "lat": "4.94847251236767", 
       "lon": "52.3900274537443", 
       "name": "Purmerweg, Amsterdam", 
       "id": "010062"
     }, 
     {
       "lat": "4.94870790153115", 
       "lon": "52.3899923748341", 
       "name": "Purmerweg, Amsterdam", 
       "id": "010072"
     }, 
     {
       "lat": "4.94939236254576", 
       "lon": "52.3876221677837", 
       "name": "Wognumerplantsoen, Amsterdam", 
       "id": "010082"
     }, 
     {
       "lat": "4.94958562329546", 
       "lon": "52.3873892031075", 
       "name": "Wognumerplantsoen, Amsterdam", 
       "id": "010092"
     }, 
     {
       "lat": "4.95370567382795", 
       "lon": "52.3866673672451", 
       "name": "Schellingwouderdijk 83, Amsterdam", 
       "id": "010102"
     }, 
     {
       "lat": "4.95369054599027", 
       "lon": "52.3867122501222", 
       "name": "Schellingwouderdijk 83, Amsterdam", 
       "id": "010112"
     }, 
     {
       "lat": "4.95850342292489", 
       "lon": "52.3857231519831", 
       "name": "Schellingwouderdijk 175, Amsterdam", 
       "id": "010122"
     }, 
     {
       "lat": "4.95879796820431", 
       "lon": "52.3856433289255", 
       "name": "Schellingwouderdijk 175, Amsterdam", 
       "id": "010132"
     }, 
     {
       "lat": "4.96311853484457", 
       "lon": "52.38388831155", 
       "name": "IJdijk, Amsterdam", 
       "id": "010142"
     }, 
     {
       "lat": "4.96273476493392", 
       "lon": "52.384084665036", 
       "name": "IJdijk, Amsterdam", 
       "id": "010152"
     }, 
     {
       "lat": "4.96653327999398", 
       "lon": "52.3815906635882", 
       "name": "Liergouw, Amsterdam", 
       "id": "010162"
     }, 
     {
       "lat": "4.96659185684662", 
       "lon": "52.3816088469459", 
       "name": "Liergouw, Amsterdam", 
       "id": "010172"
     }, 
     {
       "lat": "4.9744551276631", 
       "lon": "52.3794345382752", 
       "name": "Volkstuin, Amsterdam", 
       "id": "010182"
     }, 
     {
       "lat": "4.97404090193472", 
       "lon": "52.3797566493503", 
       "name": "Volkstuin, Amsterdam", 
       "id": "010192"
     }, 
     {
       "lat": "4.97815558998447", 
       "lon": "52.376310686458", 
       "name": "Durgerdammerdijk 4, Amsterdam", 
       "id": "010202"
     }, 
     {
       "lat": "4.97849508642105", 
       "lon": "52.3761231178665", 
       "name": "Durgerdammerdijk 4, Amsterdam", 
       "id": "010212"
     }, 
     {
       "lat": "4.98614916665031", 
       "lon": "52.3757987684889", 
       "name": "Durgerdammerdijk 36, Amsterdam", 
       "id": "010222"
     }, 
     {
       "lat": "4.9862509863709", 
       "lon": "52.3759069651111", 
       "name": "Durgerdammerdijk 36, Durgerdam", 
       "id": "010232"
     }, 
     {
       "lat": "4.98880705475459", 
       "lon": "52.3774524800437", 
       "name": "Durgerdammerdijk 82, Durgerdam", 
       "id": "010242"
     }, 
     {
       "lat": "4.98842676715169", 
       "lon": "52.3772804347644", 
       "name": "Durgerdammerdijk 82, Durgerdam", 
       "id": "010252"
     }, 
     {
       "lat": "4.99121186574693", 
       "lon": "52.3778649898145", 
       "name": "Kabelhuisje, Durgerdam", 
       "id": "010262"
     }, 
     {
       "lat": "4.99195795001259", 
       "lon": "52.3781910374748", 
       "name": "Kabelhuisje, Durgerdam", 
       "id": "010272"
     }, 
     {
       "lat": "4.99692439893908", 
       "lon": "52.3795736302668", 
       "name": "Durgerdammerdijk 175, Durgerdam", 
       "id": "010282"
     }, 
     {
       "lat": "4.99828667015588", 
       "lon": "52.3799825555093", 
       "name": "Durgerdammerdijk 175, Durgerdam", 
       "id": "010292"
     }, 
     {
       "lat": "5.00218325307666", 
       "lon": "52.3811457049055", 
       "name": "Uitdammerdijk, Durgerdam", 
       "id": "010302"
     }, 
     {
       "lat": "5.0017439788671", 
       "lon": "52.3809914862265", 
       "name": "Uitdammerdijk, Durgerdam", 
       "id": "010312"
     }, 
     {
       "lat": "5.00238673574253", 
       "lon": "52.3847773697639", 
       "name": "Durgerdammergouw 37, Durgerdam", 
       "id": "010322"
     }, 
     {
       "lat": "5.00240181362048", 
       "lon": "52.3847324806053", 
       "name": "Durgerdammergouw 37, Durgerdam", 
       "id": "010332"
     }, 
     {
       "lat": "5.00268446502512", 
       "lon": "52.3877083028986", 
       "name": "Durgerdammergouw 20, Ransdorp", 
       "id": "010342"
     }, 
     {
       "lat": "5.00269907600445", 
       "lon": "52.3877173379536", 
       "name": "Durgerdammergouw 20, Ransdorp", 
       "id": "010352"
     }, 
     {
       "lat": "4.99598842469657", 
       "lon": "52.3907781184763", 
       "name": "Dorpsweg, Ransdorp", 
       "id": "010362"
     }, 
     {
       "lat": "4.9962818269144", 
       "lon": "52.3908240252501", 
       "name": "Dorpsweg, Ransdorp", 
       "id": "010372"
     }, 
     {
       "lat": "4.99417490304285", 
       "lon": "52.3931807970696", 
       "name": "Ransdorp (kerk), Ransdorp", 
       "id": "010382"
     }, 
     {
       "lat": "4.99418895638054", 
       "lon": "52.3932527446362", 
       "name": "Ransdorp (kerk), Ransdorp", 
       "id": "010392"
     }, 
     {
       "lat": "4.99572300122101", 
       "lon": "52.3958822077162", 
       "name": "Nieuwe Gouw, Ransdorp", 
       "id": "010402"
     }, 
     {
       "lat": "4.99547372031773", 
       "lon": "52.3958274579791", 
       "name": "Nieuwe Gouw, Ransdorp", 
       "id": "010412"
     }, 
     {
       "lat": "5.00434271514394", 
       "lon": "52.39640469809", 
       "name": "Bloemend.gouw 42, Ransdorp", 
       "id": "010422"
     }, 
     {
       "lat": "5.0065045709397", 
       "lon": "52.3961600122762", 
       "name": "Bloemend.gouw 42, Ransdorp", 
       "id": "010432"
     }, 
     {
       "lat": "5.01044325167459", 
       "lon": "52.3960198150312", 
       "name": "Kinselmeer, Ransdorp", 
       "id": "010442"
     }, 
     {
       "lat": "5.01057494229828", 
       "lon": "52.3960831470183", 
       "name": "Kinselmeer, Ransdorp", 
       "id": "010452"
     }, 
     {
       "lat": "5.0180957741256", 
       "lon": "52.4033238573311", 
       "name": "Bloemendalergouw 69, Amsterdam", 
       "id": "010462"
     }, 
     {
       "lat": "5.01790564929552", 
       "lon": "52.4032154138081", 
       "name": "Bloemendalergouw 69, Amsterdam", 
       "id": "010472"
     }, 
     {
       "lat": "5.02478026307411", 
       "lon": "52.4088988177275", 
       "name": "Blijkmeer, Amsterdam", 
       "id": "010482"
     }, 
     {
       "lat": "5.02479451804881", 
       "lon": "52.4089527867742", 
       "name": "Blijkmeer, Amsterdam", 
       "id": "010492"
     }, 
     {
       "lat": "5.02567003450557", 
       "lon": "52.4133234202883", 
       "name": "Bloemendalergouw 38, Holysloot", 
       "id": "010502"
     }, 
     {
       "lat": "5.02562652890759", 
       "lon": "52.4132513870202", 
       "name": "Bloemendalergouw 38, Holysloot", 
       "id": "010512"
     }, 
     {
       "lat": "5.0250683944276", 
       "lon": "52.4132047448246", 
       "name": "Holysloot, Holysloot", 
       "id": "010522"
     }, 
     {
       "lat": "4.94586484926738", 
       "lon": "52.3907817159271", 
       "name": "Purmerplein, Amsterdam", 
       "id": "010582"
     }, 
     {
       "lat": "4.94569179315146", 
       "lon": "52.390457515705", 
       "name": "Purmerplein, Amsterdam", 
       "id": "010592"
     }, 
     {
       "lat": "4.94038274773812", 
       "lon": "52.3924957781468", 
       "name": "Wervershoofstraat, Amsterdam", 
       "id": "010602"
     }, 
     {
       "lat": "4.93954321662337", 
       "lon": "52.3927083117209", 
       "name": "Wervershoofstraat, Amsterdam", 
       "id": "010612"
     }, 
     {
       "lat": "4.93413344512396", 
       "lon": "52.3944852720476", 
       "name": "Nieuwe Purmerweg, Amsterdam", 
       "id": "010622"
     }, 
     {
       "lat": "4.93450384202274", 
       "lon": "52.3941811082675", 
       "name": "Nieuwe Purmerweg, Amsterdam", 
       "id": "010632"
     }, 
     {
       "lat": "4.93243417085751", 
       "lon": "52.3982985084536", 
       "name": "Het Breed, Amsterdam", 
       "id": "010642"
     }, 
     {
       "lat": "4.93189267853271", 
       "lon": "52.3980897126734", 
       "name": "Het Breed, Amsterdam", 
       "id": "010652"
     }, 
     {
       "lat": "4.93994231177464", 
       "lon": "52.396835146984", 
       "name": "Olof Palmeplein, Amsterdam", 
       "id": "010662"
     }, 
     {
       "lat": "4.94464713713879", 
       "lon": "52.3950373150399", 
       "name": "Ilperveldstraat, Amsterdam", 
       "id": "010672"
     }, 
     {
       "lat": "4.94516213766931", 
       "lon": "52.394958349277", 
       "name": "Ilperveldstraat, Amsterdam", 
       "id": "010682"
     }, 
     {
       "lat": "4.94948015876399", 
       "lon": "52.3936082635066", 
       "name": "Werengouw, Amsterdam", 
       "id": "010692"
     }, 
     {
       "lat": "4.94809441761881", 
       "lon": "52.3940884670629", 
       "name": "Werengouw, Amsterdam", 
       "id": "010702"
     }, 
     {
       "lat": "4.95270704388519", 
       "lon": "52.3926404915734", 
       "name": "Waterlandplein, Amsterdam", 
       "id": "010712"
     }, 
     {
       "lat": "4.95362040235577", 
       "lon": "52.3923831969001", 
       "name": "Waterlandplein, Amsterdam", 
       "id": "010762"
     }, 
     {
       "lat": "4.95440516078751", 
       "lon": "52.3962687252424", 
       "name": "Dijkmanshuizenstraat, Amsterdam", 
       "id": "010772"
     }, 
     {
       "lat": "4.95475060972122", 
       "lon": "52.3954970505333", 
       "name": "Dijkmanshuizenstraat, Amsterdam", 
       "id": "010782"
     }, 
     {
       "lat": "4.95193708985396", 
       "lon": "52.3977426412575", 
       "name": "Beemsterstraat, Amsterdam", 
       "id": "010792"
     }, 
     {
       "lat": "4.9529805749831", 
       "lon": "52.3992114542161", 
       "name": "Markengouw, Amsterdam", 
       "id": "010802"
     }, 
     {
       "lat": "4.95309811620338", 
       "lon": "52.3992118850048", 
       "name": "Markengouw, Amsterdam", 
       "id": "010812"
     }, 
     {
       "lat": "4.9608404457328", 
       "lon": "52.4038955899701", 
       "name": "Zunderdorpergouw, Amsterdam", 
       "id": "010822"
     }, 
     {
       "lat": "4.96149503819081", 
       "lon": "52.4045899901416", 
       "name": "Zunderdorpergouw, Amsterdam", 
       "id": "010832"
     }, 
     {
       "lat": "4.96448168328241", 
       "lon": "52.4072969668286", 
       "name": "Kerklaan, Amsterdam", 
       "id": "010842"
     }, 
     {
       "lat": "4.96446664498884", 
       "lon": "52.4073328635954", 
       "name": "Kerklaan, Amsterdam", 
       "id": "010852"
     }, 
     {
       "lat": "4.96494290778781", 
       "lon": "52.4097881776255", 
       "name": "t Nopeind, Amsterdam", 
       "id": "010862"
     }, 
     {
       "lat": "4.96450047920145", 
       "lon": "52.409948376857", 
       "name": "t Nopeind, Amsterdam", 
       "id": "010872"
     }, 
     {
       "lat": "4.96207448055595", 
       "lon": "52.4100565358436", 
       "name": "Zunderdorp, Amsterdam", 
       "id": "010882"
     }, 
     {
       "lat": "4.95708828096035", 
       "lon": "52.4013834691705", 
       "name": "Buikslotermeerdijk, Amsterdam", 
       "id": "010892"
     }, 
     {
       "lat": "4.95716209666531", 
       "lon": "52.4013477866666", 
       "name": "Buikslotermeerdijk, Amsterdam", 
       "id": "010902"
     }, 
     {
       "lat": "4.95105697500588", 
       "lon": "52.3975956020066", 
       "name": "Beemsterstraat, Amsterdam", 
       "id": "010912"
     }, 
     {
       "lat": "4.94437993605954", 
       "lon": "52.3982538901353", 
       "name": "Th. Weeversweg, Amsterdam", 
       "id": "010922"
     }, 
     {
       "lat": "4.94449783368152", 
       "lon": "52.3982183802679", 
       "name": "Th. Weeversweg, Amsterdam", 
       "id": "010932"
     }, 
     {
       "lat": "4.94226912645328", 
       "lon": "52.3962956637144", 
       "name": "Werengouw, Amsterdam", 
       "id": "010942"
     }, 
     {
       "lat": "4.94243091516247", 
       "lon": "52.3962782960279", 
       "name": "Werengouw, Amsterdam", 
       "id": "010952"
     }, 
     {
       "lat": "4.93443141170405", 
       "lon": "52.3998340574158", 
       "name": "Buikslotermeerplein, Amsterdam", 
       "id": "010962"
     }, 
     {
       "lat": "4.93432672529787", 
       "lon": "52.4000134099535", 
       "name": "Buikslotermeerplein, Amsterdam", 
       "id": "010972"
     }, 
     {
       "lat": "4.93459183973051", 
       "lon": "52.3999515097381", 
       "name": "Buikslotermeerplein, Amsterdam", 
       "id": "010982"
     }, 
     {
       "lat": "4.93404985759903", 
       "lon": "52.3997876602824", 
       "name": "Buikslotermeerplein, Amsterdam", 
       "id": "010992"
     }, 
     {
       "lat": "4.93759395595442", 
       "lon": "52.4023896024316", 
       "name": "Bakkerswaal, Amsterdam", 
       "id": "011002"
     }, 
     {
       "lat": "4.93728703090763", 
       "lon": "52.4022266598513", 
       "name": "Bakkerswaal, Amsterdam", 
       "id": "011012"
     }, 
     {
       "lat": "4.94031166609378", 
       "lon": "52.4039187944246", 
       "name": "J.H. van Heekweg, Amsterdam", 
       "id": "011022"
     }, 
     {
       "lat": "4.94140428001285", 
       "lon": "52.4034016287192", 
       "name": "J.H. van Heekweg, Amsterdam", 
       "id": "011032"
     }, 
     {
       "lat": "4.94255438147807", 
       "lon": "52.4030104954821", 
       "name": "Mari\u00ebndaal, Amsterdam", 
       "id": "011042"
     }, 
     {
       "lat": "4.9436615506281", 
       "lon": "52.4025023512365", 
       "name": "Mari\u00ebndaal, Amsterdam", 
       "id": "011052"
     }, 
     {
       "lat": "4.94423221873946", 
       "lon": "52.4012731816313", 
       "name": "Spelderholt, Amsterdam", 
       "id": "011062"
     }, 
     {
       "lat": "4.94418993543886", 
       "lon": "52.401093270962", 
       "name": "Spelderholt, Amsterdam", 
       "id": "011072"
     }, 
     {
       "lat": "4.94436817362451", 
       "lon": "52.3994312259493", 
       "name": "J. Drijverweg, Amsterdam", 
       "id": "011082"
     }, 
     {
       "lat": "4.94420439798591", 
       "lon": "52.3996463167452", 
       "name": "J. Drijverweg, Amsterdam", 
       "id": "011092"
     }, 
     {
       "lat": "4.92847646214443", 
       "lon": "52.3945533757188", 
       "name": "Rode Kruisstraat, Amsterdam", 
       "id": "011102"
     }, 
     {
       "lat": "4.92881101107315", 
       "lon": "52.3948782261889", 
       "name": "Rode Kruisstraat, Amsterdam", 
       "id": "011112"
     }, 
     {
       "lat": "4.92695377539861", 
       "lon": "52.3926330993013", 
       "name": "Waddenweg, Amsterdam", 
       "id": "011122"
     }, 
     {
       "lat": "4.92821965337788", 
       "lon": "52.3938153936485", 
       "name": "Waddenweg, Amsterdam", 
       "id": "011132"
     }, 
     {
       "lat": "4.92492588668947", 
       "lon": "52.3898659916038", 
       "name": "Merelstraat, Amsterdam", 
       "id": "011162"
     }, 
     {
       "lat": "4.92505715543617", 
       "lon": "52.3899563804625", 
       "name": "Merelstraat, Amsterdam", 
       "id": "011172"
     }, 
     {
       "lat": "4.92267199012303", 
       "lon": "52.3862621077181", 
       "name": "Hamerstraat, Amsterdam", 
       "id": "011192"
     }, 
     {
       "lat": "4.92100016891922", 
       "lon": "52.3860038838802", 
       "name": "Hamerstraat, Amsterdam", 
       "id": "011212"
     }, 
     {
       "lat": "4.91828997695518", 
       "lon": "52.3853191091613", 
       "name": "Havikslaan, Amsterdam", 
       "id": "011222"
     }, 
     {
       "lat": "4.91760268727873", 
       "lon": "52.3850287804559", 
       "name": "Havikslaan, Amsterdam", 
       "id": "011232"
     }, 
     {
       "lat": "4.91327553323307", 
       "lon": "52.3830971684501", 
       "name": "Valkenweg, Amsterdam", 
       "id": "011242"
     }, 
     {
       "lat": "4.91377547531576", 
       "lon": "52.3830452420139", 
       "name": "Valkenweg, Amsterdam", 
       "id": "011252"
     }, 
     {
       "lat": "4.91412702749773", 
       "lon": "52.3845116381068", 
       "name": "Spreeuwenpark, Amsterdam", 
       "id": "011262"
     }, 
     {
       "lat": "4.91429589960967", 
       "lon": "52.3852043634735", 
       "name": "Spreeuwenpark, Amsterdam", 
       "id": "011272"
     }, 
     {
       "lat": "4.91499307274176", 
       "lon": "52.38594413444", 
       "name": "Kraaienplein, Amsterdam", 
       "id": "011282"
     }, 
     {
       "lat": "4.91484360575976", 
       "lon": "52.3861862055359", 
       "name": "Kraaienplein, Amsterdam", 
       "id": "011292"
     }, 
     {
       "lat": "4.91361910515745", 
       "lon": "52.3880597385453", 
       "name": "Hagedoornplein, Amsterdam", 
       "id": "011302"
     }, 
     {
       "lat": "4.91347269638974", 
       "lon": "52.3880142146778", 
       "name": "Hagedoornplein, Amsterdam", 
       "id": "011312"
     }, 
     {
       "lat": "4.91190309882782", 
       "lon": "52.3905514360079", 
       "name": "Gentiaanstraat, Amsterdam", 
       "id": "011322"
     }, 
     {
       "lat": "4.91189004714861", 
       "lon": "52.3903985933214", 
       "name": "Gentiaanstraat, Amsterdam", 
       "id": "011332"
     }, 
     {
       "lat": "4.91072840485494", 
       "lon": "52.3905017778613", 
       "name": "Hagedoornweg, Amsterdam", 
       "id": "011342"
     }, 
     {
       "lat": "4.91103447524644", 
       "lon": "52.390727700387", 
       "name": "Hagedoornweg, Amsterdam", 
       "id": "011352"
     }, 
     {
       "lat": "4.90809528435117", 
       "lon": "52.3867522847768", 
       "name": "V.d. Pekplein, Amsterdam", 
       "id": "011362"
     }, 
     {
       "lat": "4.9084309836538", 
       "lon": "52.3869513711516", 
       "name": "V.d. Pekplein, Amsterdam", 
       "id": "011372"
     }, 
     {
       "lat": "4.91315775208785", 
       "lon": "52.3927404661875", 
       "name": "Mosplein, Amsterdam", 
       "id": "011492"
     }, 
     {
       "lat": "4.9140744254679", 
       "lon": "52.3935709959993", 
       "name": "Mosplein, Amsterdam", 
       "id": "011512"
     }, 
     {
       "lat": "4.91358099036715", 
       "lon": "52.3930028014585", 
       "name": "Mosplein, Amsterdam", 
       "id": "011552"
     }, 
     {
       "lat": "4.91395682595839", 
       "lon": "52.3963297365458", 
       "name": "Sneeuwbalstraat, Amsterdam", 
       "id": "011562"
     }, 
     {
       "lat": "4.9141325500515", 
       "lon": "52.3963843643935", 
       "name": "Sneeuwbalstraat, Amsterdam", 
       "id": "011582"
     }, 
     {
       "lat": "4.91874766428354", 
       "lon": "52.3990001363418", 
       "name": "Sneeuwbalweg, Amsterdam", 
       "id": "011622"
     }, 
     {
       "lat": "4.91871913417466", 
       "lon": "52.3989191347014", 
       "name": "Sneeuwbalweg, Amsterdam", 
       "id": "011632"
     }, 
     {
       "lat": "4.91485792035047", 
       "lon": "52.4000092817953", 
       "name": "Floraweg, Amsterdam", 
       "id": "011642"
     }, 
     {
       "lat": "4.91469476595264", 
       "lon": "52.4001524334573", 
       "name": "Floraweg, Amsterdam", 
       "id": "011652"
     }, 
     {
       "lat": "4.91174426964529", 
       "lon": "52.4026212179482", 
       "name": "Barkpad, Amsterdam", 
       "id": "011662"
     }, 
     {
       "lat": "4.91007370697128", 
       "lon": "52.4049243252466", 
       "name": "Tjalkstraat, Amsterdam", 
       "id": "011672"
     }, 
     {
       "lat": "4.91116729704655", 
       "lon": "52.405719636764", 
       "name": "Tjalkstraat, Amsterdam", 
       "id": "011682"
     }, 
     {
       "lat": "4.91677440015741", 
       "lon": "52.4104875029519", 
       "name": "Voordek, Amsterdam", 
       "id": "011712"
     }, 
     {
       "lat": "4.91743030380524", 
       "lon": "52.4110024000234", 
       "name": "Voordek, Amsterdam", 
       "id": "011722"
     }, 
     {
       "lat": "4.91923662883117", 
       "lon": "52.4125284563156", 
       "name": "Tussendek, Amsterdam", 
       "id": "011732"
     }, 
     {
       "lat": "4.91996512942863", 
       "lon": "52.4131335018602", 
       "name": "Tussendek, Amsterdam", 
       "id": "011742"
     }, 
     {
       "lat": "4.92253129887859", 
       "lon": "52.4137008258056", 
       "name": "Staghof, Amsterdam", 
       "id": "011752"
     }, 
     {
       "lat": "4.92294584001133", 
       "lon": "52.4134148470824", 
       "name": "Staghof, Amsterdam", 
       "id": "011762"
     }, 
     {
       "lat": "4.92557432356289", 
       "lon": "52.4122387516498", 
       "name": "Masthof, Amsterdam", 
       "id": "011772"
     }, 
     {
       "lat": "4.92600362175275", 
       "lon": "52.4119438321059", 
       "name": "Masthof, Amsterdam", 
       "id": "011782"
     }, 
     {
       "lat": "4.92427296178752", 
       "lon": "52.4087824277206", 
       "name": "Grootzeil, Amsterdam", 
       "id": "011792"
     }, 
     {
       "lat": "4.92316229450455", 
       "lon": "52.4081848994812", 
       "name": "Grootzeil, Amsterdam", 
       "id": "011802"
     }, 
     {
       "lat": "4.92011250737817", 
       "lon": "52.4047306522849", 
       "name": "Banne Buiksloot, Amsterdam", 
       "id": "011812"
     }, 
     {
       "lat": "4.91612896321092", 
       "lon": "52.4062248019841", 
       "name": "Koopvaardersplantsoen, Amsterdam", 
       "id": "011852"
     }, 
     {
       "lat": "4.91147910747697", 
       "lon": "52.4026830669191", 
       "name": "Barkpad, Amsterdam", 
       "id": "011882"
     }, 
     {
       "lat": "4.91221431023591", 
       "lon": "52.3985247367667", 
       "name": "Pinksterbloemstraat, Amsterdam", 
       "id": "011892"
     }, 
     {
       "lat": "4.9120349188086", 
       "lon": "52.3988116221068", 
       "name": "Pinksterbloemstraat, Amsterdam", 
       "id": "011912"
     }, 
     {
       "lat": "4.90753358392013", 
       "lon": "52.3992967888162", 
       "name": "Slijperweg, Amsterdam", 
       "id": "011932"
     }, 
     {
       "lat": "4.90768138507363", 
       "lon": "52.3992164983507", 
       "name": "Slijperweg, Amsterdam", 
       "id": "011942"
     }, 
     {
       "lat": "4.90327849342131", 
       "lon": "52.4000973587063", 
       "name": "Draaierweg, Amsterdam", 
       "id": "011972"
     }, 
     {
       "lat": "4.90220178395096", 
       "lon": "52.4004704366816", 
       "name": "Draaierweg, Amsterdam", 
       "id": "011982"
     }, 
     {
       "lat": "4.89157216582937", 
       "lon": "52.4102139897645", 
       "name": "Meteorensingel, Amsterdam", 
       "id": "012032"
     }, 
     {
       "lat": "4.89107118687375", 
       "lon": "52.4103287322612", 
       "name": "Meteorensingel, Amsterdam", 
       "id": "012042"
     }, 
     {
       "lat": "4.88734705328914", 
       "lon": "52.4121465573937", 
       "name": "Maanstraat, Amsterdam", 
       "id": "012052"
     }, 
     {
       "lat": "4.88683175070795", 
       "lon": "52.4122252710201", 
       "name": "Maanstraat, Amsterdam", 
       "id": "012062"
     }, 
     {
       "lat": "4.88482125907202", 
       "lon": "52.4132503417336", 
       "name": "Plejadenplein, Amsterdam", 
       "id": "012072"
     }, 
     {
       "lat": "4.88139376035561", 
       "lon": "52.4147906206569", 
       "name": "Meteorenweg, Amsterdam", 
       "id": "012082"
     }, 
     {
       "lat": "4.88130639520665", 
       "lon": "52.4147183465595", 
       "name": "Meteorenweg, Amsterdam", 
       "id": "012092"
     }, 
     {
       "lat": "4.88262341112984", 
       "lon": "52.4165214896689", 
       "name": "Kometensingel, Amsterdam", 
       "id": "012102"
     }, 
     {
       "lat": "4.88284265737672", 
       "lon": "52.4166302747273", 
       "name": "Kometensingel, Amsterdam", 
       "id": "012112"
     }, 
     {
       "lat": "4.88209420071101", 
       "lon": "52.4203929036734", 
       "name": "Oostzanerdijk, Amsterdam", 
       "id": "012122"
     }, 
     {
       "lat": "4.88094773798705", 
       "lon": "52.4203790234866", 
       "name": "Oostzanerdijk, Amsterdam", 
       "id": "012132"
     }, 
     {
       "lat": "4.88405250931575", 
       "lon": "52.4201136311049", 
       "name": "Bovenkruier, Amsterdam", 
       "id": "012142"
     }, 
     {
       "lat": "4.88413876678444", 
       "lon": "52.4202847622346", 
       "name": "Bovenkruier, Amsterdam", 
       "id": "012152"
     }, 
     {
       "lat": "4.88551819978193", 
       "lon": "52.4178999016031", 
       "name": "Petmolen, Amsterdam", 
       "id": "012162"
     }, 
     {
       "lat": "4.88623176875153", 
       "lon": "52.4171928979074", 
       "name": "Petmolen, Amsterdam", 
       "id": "012192"
     }, 
     {
       "lat": "4.89218131687882", 
       "lon": "52.4162023010542", 
       "name": "Standerdmolen, Amsterdam", 
       "id": "012222"
     }, 
     {
       "lat": "4.89326788051325", 
       "lon": "52.4163056994352", 
       "name": "Standerdmolen, Amsterdam", 
       "id": "012232"
     }, 
     {
       "lat": "4.89561337559426", 
       "lon": "52.4155515053862", 
       "name": "Appelweg, Amsterdam", 
       "id": "012242"
     }, 
     {
       "lat": "4.89540481033605", 
       "lon": "52.4158022934734", 
       "name": "Appelweg, Amsterdam", 
       "id": "012252"
     }, 
     {
       "lat": "4.89870167345128", 
       "lon": "52.4127421626262", 
       "name": "Druivenstraat, Amsterdam", 
       "id": "012262"
     }, 
     {
       "lat": "4.89810365835102", 
       "lon": "52.4123262644236", 
       "name": "Druivenstraat, Amsterdam", 
       "id": "012272"
     }, 
     {
       "lat": "4.89555383993841", 
       "lon": "52.4103204559614", 
       "name": "Ananasplein, Amsterdam", 
       "id": "012282"
     }, 
     {
       "lat": "4.89610821296711", 
       "lon": "52.4106912482866", 
       "name": "Ananasplein, Amsterdam", 
       "id": "012292"
     }, 
     {
       "lat": "4.95210479073265", 
       "lon": "52.3971231108343", 
       "name": "Beemsterstraat, Amsterdam", 
       "id": "012372"
     }, 
     {
       "lat": "4.9136421613209", 
       "lon": "52.4079045628016", 
       "name": "Statenjachtstraat, Amsterdam", 
       "id": "012772"
     }, 
     {
       "lat": "4.91380381150113", 
       "lon": "52.4079052088317", 
       "name": "Statenjachtstraat, Amsterdam", 
       "id": "012782"
     }, 
     {
       "lat": "4.90574743181754", 
       "lon": "52.4014106282231", 
       "name": "Draaierweg, Amsterdam", 
       "id": "012992"
     }, 
     {
       "lat": "4.96821385053878", 
       "lon": "52.3871509865679", 
       "name": "Volkstuin, Amsterdam", 
       "id": "013242"
     }, 
     {
       "lat": "4.96871682817154", 
       "lon": "52.3867752838648", 
       "name": "Volkstuin, Amsterdam", 
       "id": "013252"
     }, 
     {
       "lat": "5.00869463519219", 
       "lon": "52.3960501912525", 
       "name": "Bloemendalergouw 51, Amsterdam", 
       "id": "013262"
     }, 
     {
       "lat": "5.00862110000811", 
       "lon": "52.3960589438785", 
       "name": "Bloemendalergouw 51, Amsterdam", 
       "id": "013272"
     }, 
     {
       "lat": "4.93733273486772", 
       "lon": "52.3977240289837", 
       "name": "Het Breed, Amsterdam", 
       "id": "013282"
     }, 
     {
       "lat": "4.91815605124492", 
       "lon": "52.4076978287442", 
       "name": "Banneplein, Amsterdam", 
       "id": "013322"
     }, 
     {
       "lat": "4.9949073927603", 
       "lon": "52.391754193822", 
       "name": "Dorpsweg 38, Amsterdam", 
       "id": "013372"
     }, 
     {
       "lat": "4.99450470623545", 
       "lon": "52.3924359185802", 
       "name": "Dorpsweg 38, Amsterdam", 
       "id": "013382"
     }, 
     {
       "lat": "4.92817390469889", 
       "lon": "52.4039083368224", 
       "name": "G.J. Scheurleerweg, Amsterdam", 
       "id": "013392"
     }, 
     {
       "lat": "4.92985664564831", 
       "lon": "52.4031778592338", 
       "name": "G.J. Scheurleerweg, Amsterdam", 
       "id": "013402"
     }, 
     {
       "lat": "4.89894235591775", 
       "lon": "52.4082403492855", 
       "name": "Nageljongenstraat, Amsterdam", 
       "id": "013462"
     }, 
     {
       "lat": "4.89978099132259", 
       "lon": "52.4081539261511", 
       "name": "Nageljongenstraat, Amsterdam", 
       "id": "013472"
     }, 
     {
       "lat": "4.92231995881793", 
       "lon": "52.405826838537", 
       "name": "Oosterlengte, Amsterdam", 
       "id": "013512"
     }, 
     {
       "lat": "4.92206712861254", 
       "lon": "52.4061134503451", 
       "name": "Oosterlengte, Amsterdam", 
       "id": "013522"
     }, 
     {
       "lat": "4.92001742431007", 
       "lon": "52.4053863746183", 
       "name": "BovenIJ ziekenhuis, Amsterdam", 
       "id": "013532"
     }, 
     {
       "lat": "4.92010227660279", 
       "lon": "52.405701276346", 
       "name": "BovenIJ ziekenhuis, Amsterdam", 
       "id": "013542"
     }, 
     {
       "lat": "4.99437465079827", 
       "lon": "52.3789270776319", 
       "name": "Durgerdammerdijk 143, Amsterdam", 
       "id": "013582"
     }, 
     {
       "lat": "4.89361570923975", 
       "lon": "52.4180687236207", 
       "name": "Molenwijk, Amsterdam", 
       "id": "013592"
     }, 
     {
       "lat": "4.93968101930793", 
       "lon": "52.3994315868563", 
       "name": "Hildsven, Amsterdam", 
       "id": "013632"
     }, 
     {
       "lat": "4.93886792070332", 
       "lon": "52.3999228321758", 
       "name": "Hildsven, Amsterdam", 
       "id": "013642"
     }, 
     {
       "lat": "4.89793994605383", 
       "lon": "52.403194144961", 
       "name": "Ataturk, Amsterdam", 
       "id": "013652"
     }, 
     {
       "lat": "4.89776272617938", 
       "lon": "52.4032743017497", 
       "name": "Ataturk, Amsterdam", 
       "id": "013662"
     }, 
     {
       "lat": "4.89962422574602", 
       "lon": "52.4063737281245", 
       "name": "Tuigerstraat, Amsterdam", 
       "id": "013672"
     }, 
     {
       "lat": "4.89940578032562", 
       "lon": "52.4061930760214", 
       "name": "Tuigerstraat, Amsterdam", 
       "id": "013682"
     }, 
     {
       "lat": "4.89546712456635", 
       "lon": "52.4088640985165", 
       "name": "Pomonastraat, Amsterdam", 
       "id": "013692"
     }, 
     {
       "lat": "4.89546752352151", 
       "lon": "52.4088281496096", 
       "name": "Pomonastraat, Amsterdam", 
       "id": "013702"
     }, 
     {
       "lat": "4.90367704223295", 
       "lon": "52.382420242142", 
       "name": "Buiksloterwegveer, Amsterdam", 
       "id": "013712"
     }, 
     {
       "lat": "4.90383771760435", 
       "lon": "52.3825017872261", 
       "name": "Buiksloterwegveer, Amsterdam", 
       "id": "013722"
     }, 
     {
       "lat": "4.8935547106186", 
       "lon": "52.4182661972464", 
       "name": "Molenwijk, Amsterdam", 
       "id": "013772"
     }, 
     {
       "lat": "4.88630108495286", 
       "lon": "52.421462313539", 
       "name": "Molenaarsweg, Amsterdam", 
       "id": "013782"
     }, 
     {
       "lat": "4.88746237890381", 
       "lon": "52.4214672167502", 
       "name": "Molenaarsweg, Amsterdam", 
       "id": "013792"
     }, 
     {
       "lat": "4.89288720006051", 
       "lon": "52.4201238523887", 
       "name": "Zuideinde, Amsterdam", 
       "id": "013802"
     }, 
     {
       "lat": "4.89300529733273", 
       "lon": "52.4200794068778", 
       "name": "Zuideinde, Amsterdam", 
       "id": "013812"
     }, 
     {
       "lat": "4.90824078043683", 
       "lon": "52.4195128351671", 
       "name": "Vorticellaweg, Amsterdam", 
       "id": "013822"
     }, 
     {
       "lat": "4.90798914199686", 
       "lon": "52.4196735948134", 
       "name": "Vorticellaweg, Amsterdam", 
       "id": "013832"
     }, 
     {
       "lat": "4.96949231773109", 
       "lon": "52.3824190134004", 
       "name": "Zuiderzeeweg, Amsterdam", 
       "id": "013862"
     }, 
     {
       "lat": "4.9715048736714", 
       "lon": "52.3823811563445", 
       "name": "Zuiderzeeweg, Amsterdam", 
       "id": "013872"
     }, 
     {
       "lat": "4.97046790868186", 
       "lon": "52.3833212150918", 
       "name": "Liergouw, Amsterdam", 
       "id": "013882"
     }, 
     {
       "lat": "4.97076140374063", 
       "lon": "52.3833492103936", 
       "name": "Liergouw, Amsterdam", 
       "id": "013892"
     }, 
     {
       "lat": "4.91129097979563", 
       "lon": "52.4133596193709", 
       "name": "Kadoelenpad, Amsterdam", 
       "id": "014092"
     }, 
     {
       "lat": "4.91140267037598", 
       "lon": "52.4139083129129", 
       "name": "Kadoelenpad, Amsterdam", 
       "id": "014102"
     }, 
     {
       "lat": "4.9117003549007", 
       "lon": "52.38753975344", 
       "name": "Meidoornplein, Amsterdam", 
       "id": "014112"
     }, 
     {
       "lat": "4.91107067045407", 
       "lon": "52.3873574702456", 
       "name": "Meidoornplein, Amsterdam", 
       "id": "014122"
     }, 
     {
       "lat": "4.94011906713634", 
       "lon": "52.396790876046", 
       "name": "Olof Palmeplein, Amsterdam", 
       "id": "014142"
     }, 
     {
       "lat": "4.94016423027978", 
       "lon": "52.3966831948376", 
       "name": "Olof Palmeplein, Amsterdam", 
       "id": "014152"
     }, 
     {
       "lat": "4.93984064801955", 
       "lon": "52.3967179237871", 
       "name": "Olof Palmeplein, Amsterdam", 
       "id": "014162"
     }, 
     {
       "lat": "4.92309608290774", 
       "lon": "52.3878455994535", 
       "name": "Johan v.Hasseltweg, Amsterdam", 
       "id": "014172"
     }, 
     {
       "lat": "4.96655447431177", 
       "lon": "52.405677587493", 
       "name": "Nieuwe Gouw, Amsterdam", 
       "id": "014182"
     }, 
     {
       "lat": "4.91600953610228", 
       "lon": "52.4036358878378", 
       "name": "Fluitschipstraat, Amsterdam", 
       "id": "014202"
     }, 
     {
       "lat": "4.91618443199765", 
       "lon": "52.4037713979208", 
       "name": "Fluitschipstraat, Amsterdam", 
       "id": "014212"
     }, 
     {
       "lat": "4.89348191743556", 
       "lon": "52.4182029805922", 
       "name": "Molenwijk, Amsterdam", 
       "id": "014242"
     }, 
     {
       "lat": "4.89614595780737", 
       "lon": "52.4218720119285", 
       "name": "Lange Vonder, Amsterdam", 
       "id": "014332"
     }, 
     {
       "lat": "4.89645426109354", 
       "lon": "52.4219092395864", 
       "name": "Lange Vonder, Amsterdam", 
       "id": "014342"
     }, 
     {
       "lat": "4.89937759990737", 
       "lon": "52.4221010623716", 
       "name": "P.A. v. Heijningestraat, Amsterdam", 
       "id": "014352"
     }, 
     {
       "lat": "4.89976019963412", 
       "lon": "52.422066686335", 
       "name": "P.A. v. Heijningestraat, Amsterdam", 
       "id": "014362"
     }, 
     {
       "lat": "4.90679128050352", 
       "lon": "52.4203338278314", 
       "name": "A. v.Waertweg, Amsterdam", 
       "id": "014372"
     }, 
     {
       "lat": "4.90685173568834", 
       "lon": "52.4201812834979", 
       "name": "A. v.Waertweg, Amsterdam", 
       "id": "014382"
     }, 
     {
       "lat": "4.95696824229404", 
       "lon": "52.3925571817845", 
       "name": "Volendammerweg, Amsterdam", 
       "id": "014432"
     }, 
     {
       "lat": "4.92322753004293", 
       "lon": "52.3879180157765", 
       "name": "Johan v.Hasseltweg, Amsterdam", 
       "id": "014462"
     }, 
     {
       "lat": "4.78790845978029", 
       "lon": "52.4128447041995", 
       "name": "BP, Amsterdam", 
       "id": "020012"
     }, 
     {
       "lat": "4.80250067153393", 
       "lon": "52.4152813817555", 
       "name": "Hornweg, Amsterdam", 
       "id": "020022"
     }, 
     {
       "lat": "4.80151925249576", 
       "lon": "52.4150248790382", 
       "name": "Hornweg, Amsterdam", 
       "id": "020032"
     }, 
     {
       "lat": "4.80655140471269", 
       "lon": "52.4135037655212", 
       "name": "Elbaweg, Amsterdam", 
       "id": "020042"
     }, 
     {
       "lat": "4.80652389527752", 
       "lon": "52.4133598276659", 
       "name": "Elbaweg, Amsterdam", 
       "id": "020052"
     }, 
     {
       "lat": "4.81087527265355", 
       "lon": "52.4020026503772", 
       "name": "Corsicaweg, Amsterdam", 
       "id": "020062"
     }, 
     {
       "lat": "4.8108049972319", 
       "lon": "52.4006271889725", 
       "name": "Sardini\u00ebweg, Amsterdam", 
       "id": "020072"
     }, 
     {
       "lat": "4.82144532356954", 
       "lon": "52.3901089374011", 
       "name": "Oderweg, Amsterdam", 
       "id": "020132"
     }, 
     {
       "lat": "4.82807047300821", 
       "lon": "52.3901224250261", 
       "name": "Kapoeasweg, Amsterdam", 
       "id": "020142"
     }, 
     {
       "lat": "4.83357923121023", 
       "lon": "52.3901303285839", 
       "name": "Kastrupstraat, Amsterdam", 
       "id": "020152"
     }, 
     {
       "lat": "4.83713244039095", 
       "lon": "52.3973819874755", 
       "name": "Deccaweg 6, Amsterdam", 
       "id": "020162"
     }, 
     {
       "lat": "4.83252668269548", 
       "lon": "52.3920667497759", 
       "name": "Radarweg, Amsterdam", 
       "id": "020172"
     }, 
     {
       "lat": "4.82955906414324", 
       "lon": "52.3920707898493", 
       "name": "Isarweg, Amsterdam", 
       "id": "020182"
     }, 
     {
       "lat": "4.82465235820677", 
       "lon": "52.3920655611894", 
       "name": "Mainhavenweg, Amsterdam", 
       "id": "020192"
     }, 
     {
       "lat": "4.81965705374089", 
       "lon": "52.3920956555386", 
       "name": "Moezelhavenweg, Amsterdam", 
       "id": "020202"
     }, 
     {
       "lat": "4.83638074086392", 
       "lon": "52.3940260813449", 
       "name": "Donauweg, Amsterdam", 
       "id": "020212"
     }, 
     {
       "lat": "4.83633646620187", 
       "lon": "52.4011351450395", 
       "name": "Kwadrantweg, Amsterdam", 
       "id": "020252"
     }, 
     {
       "lat": "4.83671181418684", 
       "lon": "52.404039913541", 
       "name": "Sextantweg, Amsterdam", 
       "id": "020272"
     }, 
     {
       "lat": "4.82737028133989", 
       "lon": "52.4095055871362", 
       "name": "Kompasweg, Amsterdam", 
       "id": "020292"
     }, 
     {
       "lat": "4.82234832550431", 
       "lon": "52.4183885377832", 
       "name": "Westhavenweg, Amsterdam", 
       "id": "020312"
     }, 
     {
       "lat": "4.8253969008461", 
       "lon": "52.4179356730966", 
       "name": "Hempontplein, Amsterdam", 
       "id": "020332"
     }, 
     {
       "lat": "4.82629537932782", 
       "lon": "52.4131495007716", 
       "name": "Kajuitweg, Amsterdam", 
       "id": "020352"
     }, 
     {
       "lat": "4.82851493394914", 
       "lon": "52.410805216643", 
       "name": "Octaanweg, Amsterdam", 
       "id": "020372"
     }, 
     {
       "lat": "4.83494624175057", 
       "lon": "52.4077525969215", 
       "name": "Benzolweg, Amsterdam", 
       "id": "020392"
     }, 
     {
       "lat": "4.8508822068668", 
       "lon": "52.4012378461257", 
       "name": "Nieuwe Hemweg, Amsterdam", 
       "id": "020432"
     }, 
     {
       "lat": "4.85656196020245", 
       "lon": "52.4054876325382", 
       "name": "Coenhavenweg, Amsterdam", 
       "id": "020462"
     }, 
     {
       "lat": "4.85899481289828", 
       "lon": "52.4048064544523", 
       "name": "Pier Amerika, Amsterdam", 
       "id": "020482"
     }, 
     {
       "lat": "4.86391562501781", 
       "lon": "52.4024914990836", 
       "name": "Pier Azi\u00eb, Amsterdam", 
       "id": "020492"
     }, 
     {
       "lat": "4.86339720676635", 
       "lon": "52.4028397270761", 
       "name": "Pier Azi\u00eb, Amsterdam", 
       "id": "020502"
     }, 
     {
       "lat": "4.86981269618898", 
       "lon": "52.4046115282785", 
       "name": "Coenhaven, Amsterdam", 
       "id": "020532"
     }, 
     {
       "lat": "4.86007466285038", 
       "lon": "52.4042090904561", 
       "name": "Pier Amerika, Amsterdam", 
       "id": "020542"
     }, 
     {
       "lat": "4.84909888069272", 
       "lon": "52.4016791427119", 
       "name": "Nieuwe Hemweg, Amsterdam", 
       "id": "020552"
     }, 
     {
       "lat": "4.86040360972626", 
       "lon": "52.3926074568673", 
       "name": "Spaarndammerdijk, Amsterdam", 
       "id": "020602"
     }, 
     {
       "lat": "4.86203678874068", 
       "lon": "52.3923990050311", 
       "name": "Spaarndammerdijk, Amsterdam", 
       "id": "020612"
     }, 
     {
       "lat": "4.84827555686603", 
       "lon": "52.3920495815293", 
       "name": "Kabelweg, Amsterdam", 
       "id": "020642"
     }, 
     {
       "lat": "4.84861768742762", 
       "lon": "52.3917006174715", 
       "name": "Kabelweg, Amsterdam", 
       "id": "020652"
     }, 
     {
       "lat": "4.84007982426053", 
       "lon": "52.3919041527032", 
       "name": "La Guardiaweg, Amsterdam", 
       "id": "020662"
     }, 
     {
       "lat": "4.84324890150706", 
       "lon": "52.3922423071558", 
       "name": "Basisweg, Amsterdam", 
       "id": "020692"
     }, 
     {
       "lat": "4.82402575115142", 
       "lon": "52.4136330561735", 
       "name": "Westhavenweg 87, Amsterdam", 
       "id": "020842"
     }, 
     {
       "lat": "4.85594041356553", 
       "lon": "52.385010888534", 
       "name": "Solebaystraat, Amsterdam", 
       "id": "020862"
     }, 
     {
       "lat": "4.85477867657364", 
       "lon": "52.3851225114823", 
       "name": "Solebaystraat, Amsterdam", 
       "id": "020872"
     }, 
     {
       "lat": "4.8637818888192", 
       "lon": "52.385198596824", 
       "name": "Vredenhof, Amsterdam", 
       "id": "020882"
     }, 
     {
       "lat": "4.86238558571042", 
       "lon": "52.3852733065897", 
       "name": "Vredenhof, Amsterdam", 
       "id": "020892"
     }, 
     {
       "lat": "4.87207750619249", 
       "lon": "52.393081225443", 
       "name": "Oostzaanstraat, Amsterdam", 
       "id": "020902"
     }, 
     {
       "lat": "4.87393173293819", 
       "lon": "52.3928106570549", 
       "name": "Oostzaanstraat, Amsterdam", 
       "id": "020912"
     }, 
     {
       "lat": "4.86901926096677", 
       "lon": "52.3932925773217", 
       "name": "Hempoint, Amsterdam", 
       "id": "020922"
     }, 
     {
       "lat": "4.86946365115786", 
       "lon": "52.3929799516825", 
       "name": "Hempoint, Amsterdam", 
       "id": "020932"
     }, 
     {
       "lat": "4.87306500645805", 
       "lon": "52.3915396343056", 
       "name": "Koogstraat, Amsterdam", 
       "id": "020942"
     }, 
     {
       "lat": "4.82028382713419", 
       "lon": "52.3901842727259", 
       "name": "Oderweg, Amsterdam", 
       "id": "020952"
     }, 
     {
       "lat": "4.826880176327", 
       "lon": "52.390152750461", 
       "name": "Kapoeasweg, Amsterdam", 
       "id": "020962"
     }, 
     {
       "lat": "4.83294713644221", 
       "lon": "52.3901633230119", 
       "name": "Kastrupstraat, Amsterdam", 
       "id": "020972"
     }, 
     {
       "lat": "4.87461562522058", 
       "lon": "52.3895690640738", 
       "name": "Zaanstraat, Amsterdam", 
       "id": "020992"
     }, 
     {
       "lat": "4.87888326928624", 
       "lon": "52.3914748711099", 
       "name": "Spaarndammerstraat, Amsterdam", 
       "id": "021022"
     }, 
     {
       "lat": "4.87765604863274", 
       "lon": "52.3921616493812", 
       "name": "Spaarndammerstraat, Amsterdam", 
       "id": "021032"
     }, 
     {
       "lat": "4.88392917246916", 
       "lon": "52.3908582941808", 
       "name": "Houtmankade, Amsterdam", 
       "id": "021042"
     }, 
     {
       "lat": "4.88283967604291", 
       "lon": "52.3910693640304", 
       "name": "Houtmankade, Amsterdam", 
       "id": "021052"
     }, 
     {
       "lat": "4.87943578369251", 
       "lon": "52.3894100736632", 
       "name": "Assendelftstraat, Amsterdam", 
       "id": "021062"
     }, 
     {
       "lat": "4.87983907948943", 
       "lon": "52.3888276023751", 
       "name": "Assendelftstraat, Amsterdam", 
       "id": "021072"
     }, 
     {
       "lat": "4.8783013451973", 
       "lon": "52.3909780495851", 
       "name": "Nova Zemblastraat, Amsterdam", 
       "id": "021082"
     }, 
     {
       "lat": "4.87812279718176", 
       "lon": "52.3911750113283", 
       "name": "Nova Zemblastraat, Amsterdam", 
       "id": "021092"
     }, 
     {
       "lat": "4.88125923672773", 
       "lon": "52.3853824048832", 
       "name": "Nassauplein, Amsterdam", 
       "id": "021102"
     }, 
     {
       "lat": "4.88146630309511", 
       "lon": "52.385257461619", 
       "name": "Nassauplein, Amsterdam", 
       "id": "021112"
     }, 
     {
       "lat": "4.88149362884358", 
       "lon": "52.3854373321593", 
       "name": "Nassauplein, Amsterdam", 
       "id": "021122"
     }, 
     {
       "lat": "4.88371477768982", 
       "lon": "52.3851591898269", 
       "name": "Haarlemmerplein, Amsterdam", 
       "id": "021131"
     }, 
     {
       "lat": "4.88371477768982", 
       "lon": "52.3851591898269", 
       "name": "Haarlemmerplein, Amsterdam", 
       "id": "021132"
     }, 
     {
       "lat": "4.88340990629229", 
       "lon": "52.3848433240808", 
       "name": "Haarlemmerplein, Amsterdam", 
       "id": "021141"
     }, 
     {
       "lat": "4.88340990629229", 
       "lon": "52.3848433240808", 
       "name": "Haarlemmerplein, Amsterdam", 
       "id": "021142"
     }, 
     {
       "lat": "4.88085163434542", 
       "lon": "52.3812013838578", 
       "name": "Nw. Willemsstraat, Amsterdam", 
       "id": "021181"
     }, 
     {
       "lat": "4.88085163434542", 
       "lon": "52.3812013838578", 
       "name": "Nw. Willemsstraat, Amsterdam", 
       "id": "021182"
     }, 
     {
       "lat": "4.88066481542189", 
       "lon": "52.3808410768579", 
       "name": "Nw. Willemsstraat, Amsterdam", 
       "id": "021191"
     }, 
     {
       "lat": "4.88066481542189", 
       "lon": "52.3808410768579", 
       "name": "Nw. Willemsstraat, Amsterdam", 
       "id": "021192"
     }, 
     {
       "lat": "4.87916368104404", 
       "lon": "52.3785427816786", 
       "name": "Marnixplein, Amsterdam", 
       "id": "021201"
     }, 
     {
       "lat": "4.87859269192833", 
       "lon": "52.378387539569", 
       "name": "Marnixplein, Amsterdam", 
       "id": "021211"
     }, 
     {
       "lat": "4.87859269192833", 
       "lon": "52.378387539569", 
       "name": "Marnixplein, Amsterdam", 
       "id": "021212"
     }, 
     {
       "lat": "4.87886084474424", 
       "lon": "52.3780561458491", 
       "name": "Marnixplein, Amsterdam", 
       "id": "021221"
     }, 
     {
       "lat": "4.87886084474424", 
       "lon": "52.3780561458491", 
       "name": "Marnixplein, Amsterdam", 
       "id": "021222"
     }, 
     {
       "lat": "4.87940757481228", 
       "lon": "52.3790471393333", 
       "name": "Marnixplein, Amsterdam", 
       "id": "021232"
     }, 
     {
       "lat": "4.87632081580923", 
       "lon": "52.3741715103732", 
       "name": "Bloemgracht, Amsterdam", 
       "id": "021251"
     }, 
     {
       "lat": "4.87632081580923", 
       "lon": "52.3741715103732", 
       "name": "Bloemgracht, Amsterdam", 
       "id": "021252"
     }, 
     {
       "lat": "4.87658140707147", 
       "lon": "52.3744961922042", 
       "name": "Bloemgracht, Amsterdam", 
       "id": "021261"
     }, 
     {
       "lat": "4.87658140707147", 
       "lon": "52.3744961922042", 
       "name": "Bloemgracht, Amsterdam", 
       "id": "021262"
     }, 
     {
       "lat": "4.87584051378698", 
       "lon": "52.3725246846879", 
       "name": "Rozengracht, Amsterdam", 
       "id": "021271"
     }, 
     {
       "lat": "4.87584051378698", 
       "lon": "52.3725246846879", 
       "name": "Rozengracht, Amsterdam", 
       "id": "021272"
     }, 
     {
       "lat": "4.87062567385618", 
       "lon": "52.3752073518201", 
       "name": "G. v.Ledenberchstraat, Amsterdam", 
       "id": "021282"
     }, 
     {
       "lat": "4.87080324883593", 
       "lon": "52.3750912860546", 
       "name": "G. v.Ledenberchstraat, Amsterdam", 
       "id": "021292"
     }, 
     {
       "lat": "4.87258831365418", 
       "lon": "52.3743890278821", 
       "name": "Hugo de Grootplein, Amsterdam", 
       "id": "021301"
     }, 
     {
       "lat": "4.87291938294865", 
       "lon": "52.3749656802019", 
       "name": "Hugo de Grootplein, Amsterdam", 
       "id": "021311"
     }, 
     {
       "lat": "4.87543238012097", 
       "lon": "52.3786255792685", 
       "name": "Fred. Hendrikplants., Amsterdam", 
       "id": "021321"
     }, 
     {
       "lat": "4.87521448106607", 
       "lon": "52.3784179200431", 
       "name": "Fred. Hendrikplants., Amsterdam", 
       "id": "021331"
     }, 
     {
       "lat": "4.8753545950796", 
       "lon": "52.3790027268195", 
       "name": "Fred. Hendrikplants., Amsterdam", 
       "id": "021362"
     }, 
     {
       "lat": "4.87173384092488", 
       "lon": "52.3796790745685", 
       "name": "Kostverlorenstraat, Amsterdam", 
       "id": "021372"
     }, 
     {
       "lat": "4.87170624484231", 
       "lon": "52.379526163385", 
       "name": "Kostverlorenstraat, Amsterdam", 
       "id": "021382"
     }, 
     {
       "lat": "4.8711266322251", 
       "lon": "52.3813751066114", 
       "name": "Van Beuningenplein, Amsterdam", 
       "id": "021392"
     }, 
     {
       "lat": "4.87111372375051", 
       "lon": "52.3812222593472", 
       "name": "Van Beuningenplein, Amsterdam", 
       "id": "021402"
     }, 
     {
       "lat": "4.87036873417933", 
       "lon": "52.3833940348592", 
       "name": "V.d. Hoopstraat, Amsterdam", 
       "id": "021412"
     }, 
     {
       "lat": "4.87031050893675", 
       "lon": "52.3833488422195", 
       "name": "V.d. Hoopstraat, Amsterdam", 
       "id": "021422"
     }, 
     {
       "lat": "4.87406546669804", 
       "lon": "52.3787185286327", 
       "name": "Fred. Hendrikplants., Amsterdam", 
       "id": "021432"
     }, 
     {
       "lat": "4.86990420237813", 
       "lon": "52.3841829244365", 
       "name": "Van Hallstraat, Amsterdam", 
       "id": "021451"
     }, 
     {
       "lat": "4.87476613078054", 
       "lon": "52.3854443643964", 
       "name": "Van L.Stirumstraat, Amsterdam", 
       "id": "021462"
     }, 
     {
       "lat": "4.87517697837797", 
       "lon": "52.385482092194", 
       "name": "Van L.Stirumstraat, Amsterdam", 
       "id": "021472"
     }, 
     {
       "lat": "4.8751763012621", 
       "lon": "52.3842687501288", 
       "name": "Van L.Stirumstraat, Amsterdam", 
       "id": "021481"
     }, 
     {
       "lat": "4.87489536844825", 
       "lon": "52.38442931373", 
       "name": "Van L.Stirumstraat, Amsterdam", 
       "id": "021491"
     }, 
     {
       "lat": "4.87717266523869", 
       "lon": "52.3830999762765", 
       "name": "De Wittenkade, Amsterdam", 
       "id": "021501"
     }, 
     {
       "lat": "4.87695049599985", 
       "lon": "52.3832607978166", 
       "name": "De Wittenkade, Amsterdam", 
       "id": "021511"
     }, 
     {
       "lat": "4.8790639937583", 
       "lon": "52.3808342185825", 
       "name": "Nassaukade, Amsterdam", 
       "id": "021521"
     }, 
     {
       "lat": "4.87920529860459", 
       "lon": "52.3813201607332", 
       "name": "Nassaukade, Amsterdam", 
       "id": "021531"
     }, 
     {
       "lat": "4.87052562673417", 
       "lon": "52.3711894037821", 
       "name": "De Clercqstraat, Amsterdam", 
       "id": "021541"
     }, 
     {
       "lat": "4.86360045461441", 
       "lon": "52.3707095947209", 
       "name": "Willem de Zwijgerlaan, Amsterdam", 
       "id": "021551"
     }, 
     {
       "lat": "4.86425032330506", 
       "lon": "52.3703889085805", 
       "name": "Willem de Zwijgerlaan, Amsterdam", 
       "id": "021561"
     }, 
     {
       "lat": "4.86009649149462", 
       "lon": "52.371484967582", 
       "name": "Adm. de Ruijterweg, Amsterdam", 
       "id": "021571"
     }, 
     {
       "lat": "4.86096515211215", 
       "lon": "52.371291101488", 
       "name": "Adm. de Ruijterweg, Amsterdam", 
       "id": "021581"
     }, 
     {
       "lat": "4.85943146561203", 
       "lon": "52.37184151435", 
       "name": "Jan Evertsenstraat, Amsterdam", 
       "id": "021592"
     }, 
     {
       "lat": "4.81968700912831", 
       "lon": "52.3920508604803", 
       "name": "Moezelhavenweg, Amsterdam", 
       "id": "021602"
     }, 
     {
       "lat": "4.82471168860082", 
       "lon": "52.3920209043977", 
       "name": "Mainhavenweg, Amsterdam", 
       "id": "021612"
     }, 
     {
       "lat": "4.82859008640988", 
       "lon": "52.3920212850422", 
       "name": "Isarweg, Amsterdam", 
       "id": "021622"
     }, 
     {
       "lat": "4.85776628731152", 
       "lon": "52.3772536795765", 
       "name": "De Rijpstraat, Amsterdam", 
       "id": "021641"
     }, 
     {
       "lat": "4.85776628731152", 
       "lon": "52.3772536795765", 
       "name": "De Rijpstraat, Amsterdam", 
       "id": "021642"
     }, 
     {
       "lat": "4.85548443157154", 
       "lon": "52.3801644643579", 
       "name": "Bos en Lommerweg, Amsterdam", 
       "id": "021661"
     }, 
     {
       "lat": "4.85548443157154", 
       "lon": "52.3801644643579", 
       "name": "Bos en Lommerweg, Amsterdam", 
       "id": "021662"
     }, 
     {
       "lat": "4.85379788503538", 
       "lon": "52.3811814792745", 
       "name": "Bos en Lommerweg, Amsterdam", 
       "id": "021671"
     }, 
     {
       "lat": "4.85379788503538", 
       "lon": "52.3811814792745", 
       "name": "Bos en Lommerweg, Amsterdam", 
       "id": "021672"
     }, 
     {
       "lat": "4.85218632182505", 
       "lon": "52.3820639932387", 
       "name": "Wiltzanghlaan, Amsterdam", 
       "id": "021691"
     }, 
     {
       "lat": "4.85218632182505", 
       "lon": "52.3820639932387", 
       "name": "Wiltzanghlaan, Amsterdam", 
       "id": "021692"
     }, 
     {
       "lat": "4.8506046124171", 
       "lon": "52.3829016820057", 
       "name": "Wiltzanghlaan, Amsterdam", 
       "id": "021711"
     }, 
     {
       "lat": "4.8506046124171", 
       "lon": "52.3829016820057", 
       "name": "Wiltzanghlaan, Amsterdam", 
       "id": "021712"
     }, 
     {
       "lat": "4.84747301510819", 
       "lon": "52.3843614361425", 
       "name": "Haarlemmerweg, Amsterdam", 
       "id": "021731"
     }, 
     {
       "lat": "4.84747301510819", 
       "lon": "52.3843614361425", 
       "name": "Haarlemmerweg, Amsterdam", 
       "id": "021732"
     }, 
     {
       "lat": "4.84749888962845", 
       "lon": "52.3846491609591", 
       "name": "Haarlemmerweg, Amsterdam", 
       "id": "021751"
     }, 
     {
       "lat": "4.84749888962845", 
       "lon": "52.3846491609591", 
       "name": "Haarlemmerweg, Amsterdam", 
       "id": "021752"
     }, 
     {
       "lat": "4.85520994582655", 
       "lon": "52.3810080769986", 
       "name": "Bos en Lommerweg, Amsterdam", 
       "id": "021772"
     }, 
     {
       "lat": "4.86694884386641", 
       "lon": "52.3756765908175", 
       "name": "Markthallen, Amsterdam", 
       "id": "021822"
     }, 
     {
       "lat": "4.86666888519476", 
       "lon": "52.3757562499091", 
       "name": "Markthallen, Amsterdam", 
       "id": "021832"
     }, 
     {
       "lat": "4.86033554941352", 
       "lon": "52.374847441853", 
       "name": "Bestev\u00e2erstraat, Amsterdam", 
       "id": "021842"
     }, 
     {
       "lat": "4.87289799499298", 
       "lon": "52.392006268878", 
       "name": "Zaanhof, Amsterdam", 
       "id": "021892"
     }, 
     {
       "lat": "4.85695362207343", 
       "lon": "52.3788947962067", 
       "name": "Karel Doormanstraat, Amsterdam", 
       "id": "021901"
     }, 
     {
       "lat": "4.85695362207343", 
       "lon": "52.3788947962067", 
       "name": "Karel Doormanstraat, Amsterdam", 
       "id": "021902"
     }, 
     {
       "lat": "4.83201090425405", 
       "lon": "52.40744228345", 
       "name": "Sonthaven, Amsterdam", 
       "id": "021912"
     }, 
     {
       "lat": "4.80875218686413", 
       "lon": "52.3946673132944", 
       "name": "Hornhaven, Amsterdam", 
       "id": "021942"
     }, 
     {
       "lat": "4.80743999676627", 
       "lon": "52.3950204063877", 
       "name": "Hornhaven, Amsterdam", 
       "id": "021972"
     }, 
     {
       "lat": "4.7848727559249", 
       "lon": "52.3918070197116", 
       "name": "Pleimuiden, Amsterdam", 
       "id": "022002"
     }, 
     {
       "lat": "4.7808768646888", 
       "lon": "52.3918046055299", 
       "name": "Abberdaan, Amsterdam", 
       "id": "022012"
     }, 
     {
       "lat": "4.80802973709923", 
       "lon": "52.4049816779841", 
       "name": "Mallorcaweg, Amsterdam", 
       "id": "022022"
     }, 
     {
       "lat": "4.83725471443068", 
       "lon": "52.3993688361851", 
       "name": "Deccaweg 20, Amsterdam", 
       "id": "022152"
     }, 
     {
       "lat": "4.83883195546213", 
       "lon": "52.4013354653046", 
       "name": "Deccaweg 26, Amsterdam", 
       "id": "022172"
     }, 
     {
       "lat": "4.85941442956659", 
       "lon": "52.3720391684881", 
       "name": "Jan Evertsenstraat, Amsterdam", 
       "id": "022202"
     }, 
     {
       "lat": "4.85842078968354", 
       "lon": "52.3753242436002", 
       "name": "Jan v.Galenstraat, Amsterdam", 
       "id": "022211"
     }, 
     {
       "lat": "4.85842078968354", 
       "lon": "52.3753242436002", 
       "name": "Jan v.Galenstraat, Amsterdam", 
       "id": "022212"
     }, 
     {
       "lat": "4.85874501405291", 
       "lon": "52.3739955075812", 
       "name": "Jan v.Galenstraat, Amsterdam", 
       "id": "022221"
     }, 
     {
       "lat": "4.85874501405291", 
       "lon": "52.3739955075812", 
       "name": "Jan v.Galenstraat, Amsterdam", 
       "id": "022222"
     }, 
     {
       "lat": "4.8360314673694", 
       "lon": "52.4055736441966", 
       "name": "Radarweg, Amsterdam", 
       "id": "022272"
     }, 
     {
       "lat": "4.83690540195602", 
       "lon": "52.3896335305186", 
       "name": "Station Sloterdijk, Amsterdam", 
       "id": "022282"
     }, 
     {
       "lat": "4.8369372346183", 
       "lon": "52.3894359487359", 
       "name": "Station Sloterdijk, Amsterdam", 
       "id": "022292"
     }, 
     {
       "lat": "4.83692578044376", 
       "lon": "52.3891752518249", 
       "name": "Station Sloterdijk, Amsterdam", 
       "id": "022302"
     }, 
     {
       "lat": "4.83702562594335", 
       "lon": "52.3882320056695", 
       "name": "Station Sloterdijk, Amsterdam", 
       "id": "022401"
     }, 
     {
       "lat": "4.83694158504853", 
       "lon": "52.389085448119", 
       "name": "Station Sloterdijk, Amsterdam", 
       "id": "022412"
     }, 
     {
       "lat": "4.83694281207865", 
       "lon": "52.388986588966", 
       "name": "Station Sloterdijk, Amsterdam", 
       "id": "022422"
     }, 
     {
       "lat": "4.80382608220317", 
       "lon": "52.4039274645935", 
       "name": "Maltaweg, Amsterdam", 
       "id": "022462"
     }, 
     {
       "lat": "4.8369386847705", 
       "lon": "52.3893191151998", 
       "name": "Station Sloterdijk, Amsterdam", 
       "id": "022472"
     }, 
     {
       "lat": "4.83905114986678", 
       "lon": "52.4026217193042", 
       "name": "Deccaweg 32, Amsterdam", 
       "id": "022492"
     }, 
     {
       "lat": "4.83701815340738", 
       "lon": "52.3888341478519", 
       "name": "Station Sloterdijk, Amsterdam", 
       "id": "022502"
     }, 
     {
       "lat": "4.84718802070637", 
       "lon": "52.3969069721901", 
       "name": "Zekeringstraat, Amsterdam", 
       "id": "022522"
     }, 
     {
       "lat": "4.84741980445452", 
       "lon": "52.3971776594564", 
       "name": "Zekeringstraat, Amsterdam", 
       "id": "022532"
     }, 
     {
       "lat": "4.84726853034017", 
       "lon": "52.3927100849", 
       "name": "Kabelweg, Amsterdam", 
       "id": "022572"
     }, 
     {
       "lat": "4.84712250321301", 
       "lon": "52.3926375175091", 
       "name": "Kabelweg, Amsterdam", 
       "id": "022582"
     }, 
     {
       "lat": "4.85657708089099", 
       "lon": "52.3919522491009", 
       "name": "Contactweg, Amsterdam", 
       "id": "022592"
     }, 
     {
       "lat": "4.85432690700878", 
       "lon": "52.3921578513404", 
       "name": "Contactweg, Amsterdam", 
       "id": "022602"
     }, 
     {
       "lat": "4.80523682038111", 
       "lon": "52.3994495353749", 
       "name": "Rhodosweg, Amsterdam", 
       "id": "022632"
     }, 
     {
       "lat": "4.79997365128364", 
       "lon": "52.4129770222363", 
       "name": "Australi\u00ebhavenweg, Amsterdam", 
       "id": "022642"
     }, 
     {
       "lat": "4.80063851179737", 
       "lon": "52.4049453103963", 
       "name": "Amerikahavenweg, Amsterdam", 
       "id": "022652"
     }, 
     {
       "lat": "4.79628787885826", 
       "lon": "52.400600596365", 
       "name": "Azi\u00ebhavenweg, Amsterdam", 
       "id": "022662"
     }, 
     {
       "lat": "4.78857485034584", 
       "lon": "52.3918078143995", 
       "name": "Bolstoen, Amsterdam", 
       "id": "022702"
     }, 
     {
       "lat": "4.84223037974852", 
       "lon": "52.4021959915347", 
       "name": "Deccaweg, Amsterdam", 
       "id": "022722"
     }, 
     {
       "lat": "4.84036370193902", 
       "lon": "52.3915189923391", 
       "name": "La Guardiaweg, Amsterdam", 
       "id": "022732"
     }, 
     {
       "lat": "4.85260542311913", 
       "lon": "52.3850677824062", 
       "name": "Van Gentstraat, Amsterdam", 
       "id": "022772"
     }, 
     {
       "lat": "4.85317889631521", 
       "lon": "52.3850164435186", 
       "name": "Van Gentstraat, Amsterdam", 
       "id": "022782"
     }, 
     {
       "lat": "4.79753485554846", 
       "lon": "52.4007506140617", 
       "name": "Azi\u00ebhavenweg, Amsterdam", 
       "id": "022792"
     }, 
     {
       "lat": "4.80068194346183", 
       "lon": "52.4061049397974", 
       "name": "Amerikahavenweg, Amsterdam", 
       "id": "022812"
     }, 
     {
       "lat": "4.84825356916795", 
       "lon": "52.398691388027", 
       "name": "Dynamostraat, Amsterdam", 
       "id": "022832"
     }, 
     {
       "lat": "4.8479758370256", 
       "lon": "52.398573284074", 
       "name": "Dynamostraat, Amsterdam", 
       "id": "022842"
     }, 
     {
       "lat": "4.83492989529117", 
       "lon": "52.3854809968828", 
       "name": "Arlandaweg, Amsterdam", 
       "id": "022852"
     }, 
     {
       "lat": "4.83523621520618", 
       "lon": "52.3856531917069", 
       "name": "Arlandaweg, Amsterdam", 
       "id": "022862"
     }, 
     {
       "lat": "4.79052952113885", 
       "lon": "52.3906582594803", 
       "name": "Jarmuiden, Amsterdam", 
       "id": "022902"
     }, 
     {
       "lat": "4.79476196554692", 
       "lon": "52.3960361973052", 
       "name": "Bornhout, Amsterdam", 
       "id": "022912"
     }, 
     {
       "lat": "4.83899516838911", 
       "lon": "52.389328652194", 
       "name": "Station Sloterdijk, Amsterdam", 
       "id": "022943"
     }, 
     {
       "lat": "4.83878127901972", 
       "lon": "52.3888063746027", 
       "name": "Station Sloterdijk, Amsterdam", 
       "id": "022953"
     }, 
     {
       "lat": "4.85104451637533", 
       "lon": "52.3951089777106", 
       "name": "Isolatorweg, Amsterdam", 
       "id": "022963"
     }, 
     {
       "lat": "4.85013214301675", 
       "lon": "52.3952306719208", 
       "name": "Isolatorweg, Amsterdam", 
       "id": "022973"
     }, 
     {
       "lat": "4.79995764390486", 
       "lon": "52.413075807535", 
       "name": "Australi\u00ebhavenweg, Amsterdam", 
       "id": "022982"
     }, 
     {
       "lat": "4.84276628305562", 
       "lon": "52.3860835083388", 
       "name": "Kingsfordweg, Amsterdam", 
       "id": "022991"
     }, 
     {
       "lat": "4.84322205537769", 
       "lon": "52.3860496518883", 
       "name": "Kingsfordweg, Amsterdam", 
       "id": "023001"
     }, 
     {
       "lat": "4.87521323599934", 
       "lon": "52.3785257671682", 
       "name": "Fred. Hendrikplants., Amsterdam", 
       "id": "023012"
     }, 
     {
       "lat": "4.87549153770543", 
       "lon": "52.3785898840874", 
       "name": "Fred. Hendrikplants., Amsterdam", 
       "id": "023022"
     }, 
     {
       "lat": "4.82645265542347", 
       "lon": "52.3879487354076", 
       "name": "Plesostraat, Amsterdam", 
       "id": "023092"
     }, 
     {
       "lat": "4.82849528986388", 
       "lon": "52.3878864876501", 
       "name": "Plesostraat, Amsterdam", 
       "id": "023102"
     }, 
     {
       "lat": "4.81857055068652", 
       "lon": "52.3863203239726", 
       "name": "Seineweg, Amsterdam", 
       "id": "023112"
     }, 
     {
       "lat": "4.81892030127236", 
       "lon": "52.3865377083548", 
       "name": "Seineweg, Amsterdam", 
       "id": "023122"
     }, 
     {
       "lat": "4.82188562146922", 
       "lon": "52.3878371456748", 
       "name": "Naritaweg, Amsterdam", 
       "id": "023162"
     }, 
     {
       "lat": "4.82101807341805", 
       "lon": "52.3879049030965", 
       "name": "Naritaweg, Amsterdam", 
       "id": "023172"
     }, 
     {
       "lat": "4.8370630010822", 
       "lon": "52.3887714421862", 
       "name": "Station Sloterdijk, Amsterdam", 
       "id": "023182"
     }, 
     {
       "lat": "4.85540526587118", 
       "lon": "52.3843164329645", 
       "name": "Haarlemmerweg, Amsterdam", 
       "id": "023192"
     }, 
     {
       "lat": "4.86782041833262", 
       "lon": "52.3852703035233", 
       "name": "Van Hallstraat, Amsterdam", 
       "id": "023202"
     }, 
     {
       "lat": "4.8686416785749", 
       "lon": "52.3853817548436", 
       "name": "Van Hallstraat, Amsterdam", 
       "id": "023212"
     }, 
     {
       "lat": "4.83571809295056", 
       "lon": "52.3941488256751", 
       "name": "Donauweg, Amsterdam", 
       "id": "023242"
     }, 
     {
       "lat": "4.79752498908848", 
       "lon": "52.4136389371735", 
       "name": "Sicili\u00ebweg, Amsterdam", 
       "id": "023252"
     }, 
     {
       "lat": "4.80642920228695", 
       "lon": "52.4149771473556", 
       "name": "Capriweg, Amsterdam", 
       "id": "023262"
     }, 
     {
       "lat": "4.80561351830097", 
       "lon": "52.4155303827141", 
       "name": "Capriweg, Amsterdam", 
       "id": "023272"
     }, 
     {
       "lat": "4.79331150058352", 
       "lon": "52.3957323381792", 
       "name": "Bornhout, Amsterdam", 
       "id": "023322"
     }, 
     {
       "lat": "4.78728786999718", 
       "lon": "52.3957199567682", 
       "name": "Herwijk, Amsterdam", 
       "id": "023332"
     }, 
     {
       "lat": "4.87933716918476", 
       "lon": "52.3813476894562", 
       "name": "Nassaukade, Amsterdam", 
       "id": "023342"
     }, 
     {
       "lat": "4.80373886522363", 
       "lon": "52.4038551333675", 
       "name": "Maltaweg, Amsterdam", 
       "id": "023372"
     }, 
     {
       "lat": "4.79522625308498", 
       "lon": "52.3975754202475", 
       "name": "Westpoortweg, Amsterdam", 
       "id": "023392"
     }, 
     {
       "lat": "4.77969216650296", 
       "lon": "52.3957082035819", 
       "name": "Scharenburg, Amsterdam", 
       "id": "023422"
     }, 
     {
       "lat": "4.80519345113893", 
       "lon": "52.3993953959878", 
       "name": "Rhodosweg, Amsterdam", 
       "id": "023432"
     }, 
     {
       "lat": "4.79429319058586", 
       "lon": "52.3970314895637", 
       "name": "Westpoortweg, Amsterdam", 
       "id": "023442"
     }, 
     {
       "lat": "4.85946354610465", 
       "lon": "52.3654423887938", 
       "name": "Postjesweg, Amsterdam", 
       "id": "030031"
     }, 
     {
       "lat": "4.85951272107983", 
       "lon": "52.3650111963302", 
       "name": "Postjesweg, Amsterdam", 
       "id": "030041"
     }, 
     {
       "lat": "4.85904588259019", 
       "lon": "52.3684604069165", 
       "name": "Van Kinsbergenstraat, Amsterdam", 
       "id": "030051"
     }, 
     {
       "lat": "4.85904770160963", 
       "lon": "52.3683076234943", 
       "name": "Van Kinsbergenstraat, Amsterdam", 
       "id": "030061"
     }, 
     {
       "lat": "4.85896866004306", 
       "lon": "52.3712462602055", 
       "name": "Jan Evertsenstraat, Amsterdam", 
       "id": "030071"
     }, 
     {
       "lat": "4.85897197782384", 
       "lon": "52.3709676552979", 
       "name": "Jan Evertsenstraat, Amsterdam", 
       "id": "030081"
     }, 
     {
       "lat": "4.85851707988713", 
       "lon": "52.3647820606961", 
       "name": "Witte de Withstraat, Amsterdam", 
       "id": "030091"
     }, 
     {
       "lat": "4.85851707988713", 
       "lon": "52.3647820606961", 
       "name": "Witte de Withstraat, Amsterdam", 
       "id": "030092"
     }, 
     {
       "lat": "4.85928028224904", 
       "lon": "52.3648034419559", 
       "name": "Witte de Withstraat, Amsterdam", 
       "id": "030101"
     }, 
     {
       "lat": "4.85928028224904", 
       "lon": "52.3648034419559", 
       "name": "Witte de Withstraat, Amsterdam", 
       "id": "030102"
     }, 
     {
       "lat": "4.85237091204047", 
       "lon": "52.3643230422121", 
       "name": "Postjesweg, Amsterdam", 
       "id": "030122"
     }, 
     {
       "lat": "4.85284145911644", 
       "lon": "52.3642622528101", 
       "name": "Hoofdweg, Amsterdam", 
       "id": "030132"
     }, 
     {
       "lat": "4.85070048405705", 
       "lon": "52.3701215671855", 
       "name": "Mercatorplein, Amsterdam", 
       "id": "030221"
     }, 
     {
       "lat": "4.85070048405705", 
       "lon": "52.3701215671855", 
       "name": "Mercatorplein, Amsterdam", 
       "id": "030222"
     }, 
     {
       "lat": "4.8551992776252", 
       "lon": "52.3708788617009", 
       "name": "Marco Polostraat, Amsterdam", 
       "id": "030231"
     }, 
     {
       "lat": "4.8551992776252", 
       "lon": "52.3708788617009", 
       "name": "Marco Polostraat, Amsterdam", 
       "id": "030232"
     }, 
     {
       "lat": "4.85546271141286", 
       "lon": "52.3709519469752", 
       "name": "Marco Polostraat, Amsterdam", 
       "id": "030241"
     }, 
     {
       "lat": "4.85546271141286", 
       "lon": "52.3709519469752", 
       "name": "Marco Polostraat, Amsterdam", 
       "id": "030242"
     }, 
     {
       "lat": "4.84854599464149", 
       "lon": "52.3734192723976", 
       "name": "Jan v.Galenstraat, Amsterdam", 
       "id": "030251"
     }, 
     {
       "lat": "4.84854599464149", 
       "lon": "52.3734192723976", 
       "name": "Jan v.Galenstraat, Amsterdam", 
       "id": "030252"
     }, 
     {
       "lat": "4.84871253689325", 
       "lon": "52.3730065941121", 
       "name": "Jan v.Galenstraat, Amsterdam", 
       "id": "030261"
     }, 
     {
       "lat": "4.84871253689325", 
       "lon": "52.3730065941121", 
       "name": "Jan v.Galenstraat, Amsterdam", 
       "id": "030262"
     }, 
     {
       "lat": "4.84690855343424", 
       "lon": "52.3764406779505", 
       "name": "Erasmusgracht, Amsterdam", 
       "id": "030341"
     }, 
     {
       "lat": "4.84690855343424", 
       "lon": "52.3764406779505", 
       "name": "Erasmusgracht, Amsterdam", 
       "id": "030342"
     }, 
     {
       "lat": "4.85075580500419", 
       "lon": "52.378902831628", 
       "name": "Egidiusstraat, Amsterdam", 
       "id": "030361"
     }, 
     {
       "lat": "4.85075580500419", 
       "lon": "52.378902831628", 
       "name": "Egidiusstraat, Amsterdam", 
       "id": "030362"
     }, 
     {
       "lat": "4.85150336654182", 
       "lon": "52.3790230563139", 
       "name": "Egidiusstraat, Amsterdam", 
       "id": "030371"
     }, 
     {
       "lat": "4.85150336654182", 
       "lon": "52.3790230563139", 
       "name": "Egidiusstraat, Amsterdam", 
       "id": "030372"
     }, 
     {
       "lat": "4.85369282754914", 
       "lon": "52.3801474183808", 
       "name": "Bos en Lommerweg, Amsterdam", 
       "id": "030381"
     }, 
     {
       "lat": "4.85369282754914", 
       "lon": "52.3801474183808", 
       "name": "Bos en Lommerweg, Amsterdam", 
       "id": "030382"
     }, 
     {
       "lat": "4.85096481863919", 
       "lon": "52.3822651857535", 
       "name": "Wiltzanghlaan, Amsterdam", 
       "id": "030392"
     }, 
     {
       "lat": "4.84753378356025", 
       "lon": "52.3817822380071", 
       "name": "Granidastraat, Amsterdam", 
       "id": "030412"
     }, 
     {
       "lat": "4.84599124277412", 
       "lon": "52.3818111490696", 
       "name": "Granidastraat, Amsterdam", 
       "id": "030422"
     }, 
     {
       "lat": "4.8413815036285", 
       "lon": "52.3816372001192", 
       "name": "Akbarstraat, Amsterdam", 
       "id": "030432"
     }, 
     {
       "lat": "4.84193849043544", 
       "lon": "52.3817296433427", 
       "name": "Akbarstraat, Amsterdam", 
       "id": "030442"
     }, 
     {
       "lat": "4.83418506560296", 
       "lon": "52.3827812036014", 
       "name": "Burg. Fockstraat, Amsterdam", 
       "id": "030452"
     }, 
     {
       "lat": "4.83456838355695", 
       "lon": "52.382666152606", 
       "name": "Burg. Fockstraat, Amsterdam", 
       "id": "030462"
     }, 
     {
       "lat": "4.82795540491155", 
       "lon": "52.3829406897892", 
       "name": "L. Naarstigstraat, Amsterdam", 
       "id": "030472"
     }, 
     {
       "lat": "4.82770515834811", 
       "lon": "52.3829844463744", 
       "name": "L. Naarstigstraat, Amsterdam", 
       "id": "030482"
     }, 
     {
       "lat": "4.82706853656388", 
       "lon": "52.3810580618696", 
       "name": "Burg. Eliasstraat, Amsterdam", 
       "id": "030502"
     }, 
     {
       "lat": "4.82801719327088", 
       "lon": "52.3803704897968", 
       "name": "Burg. Eliasstraat, Amsterdam", 
       "id": "030511"
     }, 
     {
       "lat": "4.82801719327088", 
       "lon": "52.3803704897968", 
       "name": "Burg. Eliasstraat, Amsterdam", 
       "id": "030512"
     }, 
     {
       "lat": "4.82564748341911", 
       "lon": "52.3807727116398", 
       "name": "Burg. Eliasstraat, Amsterdam", 
       "id": "030521"
     }, 
     {
       "lat": "4.82564748341911", 
       "lon": "52.3807727116398", 
       "name": "Burg. Eliasstraat, Amsterdam", 
       "id": "030522"
     }, 
     {
       "lat": "4.83338854047169", 
       "lon": "52.3795239226244", 
       "name": "Burg. Fockstraat, Amsterdam", 
       "id": "030541"
     }, 
     {
       "lat": "4.83338854047169", 
       "lon": "52.3795239226244", 
       "name": "Burg. Fockstraat, Amsterdam", 
       "id": "030542"
     }, 
     {
       "lat": "4.8310777811026", 
       "lon": "52.3799175408861", 
       "name": "Burg. Fockstraat, Amsterdam", 
       "id": "030551"
     }, 
     {
       "lat": "4.8310777811026", 
       "lon": "52.3799175408861", 
       "name": "Burg. Fockstraat, Amsterdam", 
       "id": "030552"
     }, 
     {
       "lat": "4.81474540193273", 
       "lon": "52.3833718932406", 
       "name": "Ant. Moddermanstraat, Amsterdam", 
       "id": "030572"
     }, 
     {
       "lat": "4.8471814596967", 
       "lon": "52.3781495913695", 
       "name": "Bos en Lommerplein, Amsterdam", 
       "id": "030601"
     }, 
     {
       "lat": "4.8471814596967", 
       "lon": "52.3781495913695", 
       "name": "Bos en Lommerplein, Amsterdam", 
       "id": "030602"
     }, 
     {
       "lat": "4.84523268397335", 
       "lon": "52.3777811787616", 
       "name": "Bos en Lommerplein, Amsterdam", 
       "id": "030611"
     }, 
     {
       "lat": "4.84523268397335", 
       "lon": "52.3777811787616", 
       "name": "Bos en Lommerplein, Amsterdam", 
       "id": "030612"
     }, 
     {
       "lat": "4.84447007114784", 
       "lon": "52.3692932616783", 
       "name": "Adm. Helfrichstraat, Amsterdam", 
       "id": "030692"
     }, 
     {
       "lat": "4.83818316519408", 
       "lon": "52.3694889688421", 
       "name": "Jan Voermanstraat, Amsterdam", 
       "id": "030712"
     }, 
     {
       "lat": "4.83810051599643", 
       "lon": "52.3714209512062", 
       "name": "Jan Tooropstraat, Amsterdam", 
       "id": "030761"
     }, 
     {
       "lat": "4.83810051599643", 
       "lon": "52.3714209512062", 
       "name": "Jan Tooropstraat, Amsterdam", 
       "id": "030762"
     }, 
     {
       "lat": "4.83785646620936", 
       "lon": "52.3709704318175", 
       "name": "Jan Tooropstraat, Amsterdam", 
       "id": "030771"
     }, 
     {
       "lat": "4.83785646620936", 
       "lon": "52.3709704318175", 
       "name": "Jan Tooropstraat, Amsterdam", 
       "id": "030772"
     }, 
     {
       "lat": "4.83206605617153", 
       "lon": "52.3737116500365", 
       "name": "Burg. v.d. Pollstraat, Amsterdam", 
       "id": "030782"
     }, 
     {
       "lat": "4.83247923100884", 
       "lon": "52.3735518070881", 
       "name": "Burg. v.d. Pollstraat, Amsterdam", 
       "id": "030792"
     }, 
     {
       "lat": "4.82062866079596", 
       "lon": "52.3815936523332", 
       "name": "Plein '40 - '45, Amsterdam", 
       "id": "030872"
     }, 
     {
       "lat": "4.81727888340574", 
       "lon": "52.3759602364465", 
       "name": "Slotermeerlaan, Amsterdam", 
       "id": "030901"
     }, 
     {
       "lat": "4.81727888340574", 
       "lon": "52.3759602364465", 
       "name": "Slotermeerlaan, Amsterdam", 
       "id": "030902"
     }, 
     {
       "lat": "4.82076627520741", 
       "lon": "52.375419730462", 
       "name": "Slotermeerlaan, Amsterdam", 
       "id": "030911"
     }, 
     {
       "lat": "4.82076627520741", 
       "lon": "52.375419730462", 
       "name": "Slotermeerlaan, Amsterdam", 
       "id": "030912"
     }, 
     {
       "lat": "4.81373382958676", 
       "lon": "52.3764104831332", 
       "name": "Burg. v. Leeuwenlaan, Amsterdam", 
       "id": "030952"
     }, 
     {
       "lat": "4.81325120712056", 
       "lon": "52.3762553529024", 
       "name": "Burg. v. Leeuwenlaan, Amsterdam", 
       "id": "030962"
     }, 
     {
       "lat": "4.81182340155614", 
       "lon": "52.3765090681595", 
       "name": "Burg. v. Leeuwenlaan, Amsterdam", 
       "id": "030971"
     }, 
     {
       "lat": "4.81208854503062", 
       "lon": "52.376447442009", 
       "name": "Burg. v. Leeuwenlaan, Amsterdam", 
       "id": "030981"
     }, 
     {
       "lat": "4.80672187348044", 
       "lon": "52.376933556002", 
       "name": "Dr. H. Colijnstraat, Amsterdam", 
       "id": "030991"
     }, 
     {
       "lat": "4.80626640307343", 
       "lon": "52.3769492977379", 
       "name": "Dr. H. Colijnstraat, Amsterdam", 
       "id": "031001"
     }, 
     {
       "lat": "4.8030019532547", 
       "lon": "52.3772657835801", 
       "name": "Lambertus Zijlplein, Amsterdam", 
       "id": "031011"
     }, 
     {
       "lat": "4.81183518387581", 
       "lon": "52.3744689048592", 
       "name": "Confuciusplein, Amsterdam", 
       "id": "031022"
     }, 
     {
       "lat": "4.81206861593678", 
       "lon": "52.3745868798143", 
       "name": "Confuciusplein, Amsterdam", 
       "id": "031032"
     }, 
     {
       "lat": "4.80708866556432", 
       "lon": "52.3747153772692", 
       "name": "Dr. H. Colijnstraat, Amsterdam", 
       "id": "031042"
     }, 
     {
       "lat": "4.80725136768072", 
       "lon": "52.3746262967095", 
       "name": "Dr. H. Colijnstraat, Amsterdam", 
       "id": "031052"
     }, 
     {
       "lat": "4.80155175198473", 
       "lon": "52.3747600218595", 
       "name": "Troelstralaan, Amsterdam", 
       "id": "031062"
     }, 
     {
       "lat": "4.80029551552393", 
       "lon": "52.3709250120992", 
       "name": "Willinklaan, Amsterdam", 
       "id": "031072"
     }, 
     {
       "lat": "4.80080457924476", 
       "lon": "52.3679615689675", 
       "name": "Herman Bonpad, Amsterdam", 
       "id": "031082"
     }, 
     {
       "lat": "4.8006449248886", 
       "lon": "52.3689314579183", 
       "name": "Herman Bonpad, Amsterdam", 
       "id": "031092"
     }, 
     {
       "lat": "4.80042504691475", 
       "lon": "52.3711233851179", 
       "name": "Willinklaan, Amsterdam", 
       "id": "031102"
     }, 
     {
       "lat": "4.8020629742808", 
       "lon": "52.3749692679573", 
       "name": "Troelstralaan, Amsterdam", 
       "id": "031112"
     }, 
     {
       "lat": "4.80098757278077", 
       "lon": "52.3752245936773", 
       "name": "Nolensstraat, Amsterdam", 
       "id": "031132"
     }, 
     {
       "lat": "4.80079382338961", 
       "lon": "52.375439340597", 
       "name": "De Sav. Lohmanstraat, Amsterdam", 
       "id": "031142"
     }, 
     {
       "lat": "4.79770136090188", 
       "lon": "52.3760800912984", 
       "name": "De Sav. Lohmanstraat, Amsterdam", 
       "id": "031152"
     }, 
     {
       "lat": "4.79756692837268", 
       "lon": "52.37625018945", 
       "name": "De Sav. Lohmanstraat, Amsterdam", 
       "id": "031162"
     }, 
     {
       "lat": "4.79790168421397", 
       "lon": "52.3786875394576", 
       "name": "Sam van Houtenstraat, Amsterdam", 
       "id": "031172"
     }, 
     {
       "lat": "4.79800483977326", 
       "lon": "52.379766583824", 
       "name": "Sam van Houtenstraat, Amsterdam", 
       "id": "031182"
     }, 
     {
       "lat": "4.79773987916908", 
       "lon": "52.3820211918133", 
       "name": "Aalbersestraat, Amsterdam", 
       "id": "031212"
     }, 
     {
       "lat": "4.7989696248934", 
       "lon": "52.3823239027906", 
       "name": "Aalbersestraat, Amsterdam", 
       "id": "031222"
     }, 
     {
       "lat": "4.80565093157932", 
       "lon": "52.3824467809157", 
       "name": "Dr. H. Colijnstraat, Amsterdam", 
       "id": "031232"
     }, 
     {
       "lat": "4.80663318379998", 
       "lon": "52.3825864169008", 
       "name": "Dr. H. Colijnstraat, Amsterdam", 
       "id": "031242"
     }, 
     {
       "lat": "4.81338031145668", 
       "lon": "52.383302372168", 
       "name": "Ant. Moddermanstraat, Amsterdam", 
       "id": "031252"
     }, 
     {
       "lat": "4.82112410235028", 
       "lon": "52.3807511743011", 
       "name": "Plein '40 - '45, Amsterdam", 
       "id": "031291"
     }, 
     {
       "lat": "4.82112410235028", 
       "lon": "52.3807511743011", 
       "name": "Plein '40 - '45, Amsterdam", 
       "id": "031292"
     }, 
     {
       "lat": "4.82267512913204", 
       "lon": "52.3812079656504", 
       "name": "Plein '40 - '45, Amsterdam", 
       "id": "031301"
     }, 
     {
       "lat": "4.82267512913204", 
       "lon": "52.3812079656504", 
       "name": "Plein '40 - '45, Amsterdam", 
       "id": "031302"
     }, 
     {
       "lat": "4.81967015375274", 
       "lon": "52.3773019089272", 
       "name": "Lod. v. Deysselstraat, Amsterdam", 
       "id": "031311"
     }, 
     {
       "lat": "4.81967015375274", 
       "lon": "52.3773019089272", 
       "name": "Lod. v. Deysselstraat, Amsterdam", 
       "id": "031312"
     }, 
     {
       "lat": "4.81950083467618", 
       "lon": "52.3767618324004", 
       "name": "Lod. v. Deysselstraat, Amsterdam", 
       "id": "031321"
     }, 
     {
       "lat": "4.81950083467618", 
       "lon": "52.3767618324004", 
       "name": "Lod. v. Deysselstraat, Amsterdam", 
       "id": "031322"
     }, 
     {
       "lat": "4.81595468070295", 
       "lon": "52.3704533479306", 
       "name": "Sloterparkbad, Amsterdam", 
       "id": "031352"
     }, 
     {
       "lat": "4.83827025759716", 
       "lon": "52.3683838794396", 
       "name": "Hart Nibbrigstraat, Amsterdam", 
       "id": "031392"
     }, 
     {
       "lat": "4.83874208916602", 
       "lon": "52.3682242866406", 
       "name": "Hart Nibbrigstraat, Amsterdam", 
       "id": "031402"
     }, 
     {
       "lat": "4.84038338473809", 
       "lon": "52.3661017814786", 
       "name": "Piet Mondriaanstraat, Amsterdam", 
       "id": "031412"
     }, 
     {
       "lat": "4.84038870192079", 
       "lon": "52.3656703938458", 
       "name": "Piet Mondriaanstraat, Amsterdam", 
       "id": "031422"
     }, 
     {
       "lat": "4.80409377405017", 
       "lon": "52.3824660866832", 
       "name": "J. Cabeliaustraat, Amsterdam", 
       "id": "031452"
     }, 
     {
       "lat": "4.85011077679433", 
       "lon": "52.3703166238155", 
       "name": "Mercatorplein, Amsterdam", 
       "id": "031502"
     }, 
     {
       "lat": "4.80338376591286", 
       "lon": "52.3772676667548", 
       "name": "Lambertus Zijlplein, Amsterdam", 
       "id": "031571"
     }, 
     {
       "lat": "4.83794985820319", 
       "lon": "52.3788441246513", 
       "name": "Burg.de Vlugtlaan, Amsterdam", 
       "id": "031621"
     }, 
     {
       "lat": "4.83794985820319", 
       "lon": "52.3788441246513", 
       "name": "Burg.de Vlugtlaan, Amsterdam", 
       "id": "031622"
     }, 
     {
       "lat": "4.83793550644732", 
       "lon": "52.3788170948844", 
       "name": "Burg.de Vlugtlaan, Amsterdam", 
       "id": "031631"
     }, 
     {
       "lat": "4.83793550644732", 
       "lon": "52.3788170948844", 
       "name": "Burg.de Vlugtlaan, Amsterdam", 
       "id": "031632"
     }, 
     {
       "lat": "4.84310814554695", 
       "lon": "52.3642089315661", 
       "name": "Nachtwachtlaan, Amsterdam", 
       "id": "031642"
     }, 
     {
       "lat": "4.84331510988409", 
       "lon": "52.3640930417638", 
       "name": "Nachtwachtlaan, Amsterdam", 
       "id": "031652"
     }, 
     {
       "lat": "4.84650406212504", 
       "lon": "52.3770949358974", 
       "name": "Bos en Lommerplein, Amsterdam", 
       "id": "031671"
     }, 
     {
       "lat": "4.84650406212504", 
       "lon": "52.3770949358974", 
       "name": "Bos en Lommerplein, Amsterdam", 
       "id": "031672"
     }, 
     {
       "lat": "4.85152131186464", 
       "lon": "52.3702421244142", 
       "name": "Mercatorplein, Amsterdam", 
       "id": "031681"
     }, 
     {
       "lat": "4.85152131186464", 
       "lon": "52.3702421244142", 
       "name": "Mercatorplein, Amsterdam", 
       "id": "031682"
     }, 
     {
       "lat": "4.83601030087773", 
       "lon": "52.3730110575894", 
       "name": "Jan v.Galenstraat, Amsterdam", 
       "id": "031691"
     }, 
     {
       "lat": "4.83495016086081", 
       "lon": "52.3732397989636", 
       "name": "Jan v.Galenstraat, Amsterdam", 
       "id": "031701"
     }, 
     {
       "lat": "4.82768172793924", 
       "lon": "52.3743650938204", 
       "name": "Burg. Rendorpstraat, Amsterdam", 
       "id": "031711"
     }, 
     {
       "lat": "4.82768172793924", 
       "lon": "52.3743650938204", 
       "name": "Burg. Rendorpstraat, Amsterdam", 
       "id": "031712"
     }, 
     {
       "lat": "4.82691701469618", 
       "lon": "52.37445135515", 
       "name": "Burg. Rendorpstraat, Amsterdam", 
       "id": "031721"
     }, 
     {
       "lat": "4.82691701469618", 
       "lon": "52.37445135515", 
       "name": "Burg. Rendorpstraat, Amsterdam", 
       "id": "031722"
     }, 
     {
       "lat": "4.81863063027331", 
       "lon": "52.3747623764078", 
       "name": "Burg. Ro\u00ebllstraat, Amsterdam", 
       "id": "031741"
     }, 
     {
       "lat": "4.81883091261132", 
       "lon": "52.3751767745748", 
       "name": "Burg. Ro\u00ebllstraat, Amsterdam", 
       "id": "031751"
     }, 
     {
       "lat": "4.81890352518577", 
       "lon": "52.3729481602423", 
       "name": "Sloterpark, Amsterdam", 
       "id": "031761"
     }, 
     {
       "lat": "4.84991402080105", 
       "lon": "52.3708010690261", 
       "name": "Mercatorplein, Amsterdam", 
       "id": "031782"
     }, 
     {
       "lat": "4.84386621541995", 
       "lon": "52.3694432836966", 
       "name": "Adm. Helfrichstraat, Amsterdam", 
       "id": "031791"
     }, 
     {
       "lat": "4.8445859924362", 
       "lon": "52.3694196214417", 
       "name": "Adm. Helfrichstraat, Amsterdam", 
       "id": "031801"
     }, 
     {
       "lat": "4.83788684220034", 
       "lon": "52.3697033003454", 
       "name": "Jan Voermanstraat, Amsterdam", 
       "id": "031811"
     }, 
     {
       "lat": "4.83851964216765", 
       "lon": "52.369589393899", 
       "name": "Jan Voermanstraat, Amsterdam", 
       "id": "031821"
     }, 
     {
       "lat": "4.81901032049614", 
       "lon": "52.3829520344611", 
       "name": "Burg.de Vlugtlaan, Amsterdam", 
       "id": "031872"
     }, 
     {
       "lat": "4.81861607588164", 
       "lon": "52.3827703874147", 
       "name": "Burg.de Vlugtlaan, Amsterdam", 
       "id": "031882"
     }, 
     {
       "lat": "4.7911520956052", 
       "lon": "52.3815028762921", 
       "name": "J.M. den Uylstraat, Amsterdam", 
       "id": "031902"
     }, 
     {
       "lat": "4.79000388750152", 
       "lon": "52.3816948218473", 
       "name": "J.M. den Uylstraat, Amsterdam", 
       "id": "031912"
     }, 
     {
       "lat": "4.78809670793823", 
       "lon": "52.3804448768856", 
       "name": "Frle. Wttewaalpad, Amsterdam", 
       "id": "031922"
     }, 
     {
       "lat": "4.78804512795577", 
       "lon": "52.3799143378354", 
       "name": "Frle. Wttewaalpad, Amsterdam", 
       "id": "031932"
     }, 
     {
       "lat": "4.79047532431463", 
       "lon": "52.3794053193053", 
       "name": "W. Dreesplantsoen, Amsterdam", 
       "id": "031942"
     }, 
     {
       "lat": "4.79060798000384", 
       "lon": "52.3793700366903", 
       "name": "W. Dreesplantsoen, Amsterdam", 
       "id": "031952"
     }, 
     {
       "lat": "4.79740929137301", 
       "lon": "52.3792692922651", 
       "name": "Sam van Houtenstraat, Amsterdam", 
       "id": "031962"
     }, 
     {
       "lat": "4.85237822727589", 
       "lon": "52.3673699212563", 
       "name": "W. Schoutenstraat, Amsterdam", 
       "id": "031972"
     }, 
     {
       "lat": "4.8525879981934", 
       "lon": "52.3670203466812", 
       "name": "W. Schoutenstraat, Amsterdam", 
       "id": "031982"
     }, 
     {
       "lat": "4.795248185895", 
       "lon": "52.3816312764835", 
       "name": "Pieter Postpad, Amsterdam", 
       "id": "032002"
     }, 
     {
       "lat": "4.79490979547078", 
       "lon": "52.3816745231797", 
       "name": "Pieter Postpad, Amsterdam", 
       "id": "032012"
     }, 
     {
       "lat": "4.83531218998491", 
       "lon": "52.3724685409447", 
       "name": "Jan v.Galenstraat, Amsterdam", 
       "id": "032023"
     }, 
     {
       "lat": "4.8349219999381", 
       "lon": "52.3719634077638", 
       "name": "Jan v.Galenstraat, Amsterdam", 
       "id": "032033"
     }, 
     {
       "lat": "4.8384641976326", 
       "lon": "52.3800059265208", 
       "name": "Burg.de Vlugtlaan, Amsterdam", 
       "id": "032043"
     }, 
     {
       "lat": "4.83808848024672", 
       "lon": "52.3795098596795", 
       "name": "Burg.de Vlugtlaan, Amsterdam", 
       "id": "032053"
     }, 
     {
       "lat": "4.83587580108293", 
       "lon": "52.3731991740019", 
       "name": "Jan v.Galenstraat, Amsterdam", 
       "id": "032152"
     }, 
     {
       "lat": "4.83649709672417", 
       "lon": "52.3728335678767", 
       "name": "Jan v.Galenstraat, Amsterdam", 
       "id": "032162"
     }, 
     {
       "lat": "4.83320989915276", 
       "lon": "52.3703106511143", 
       "name": "Alhambralaan, Amsterdam", 
       "id": "032172"
     }, 
     {
       "lat": "4.83309333440348", 
       "lon": "52.3702382036288", 
       "name": "Alhambralaan, Amsterdam", 
       "id": "032182"
     }, 
     {
       "lat": "4.83618153179061", 
       "lon": "52.3698661432492", 
       "name": "Jan Evertsenstraat, Amsterdam", 
       "id": "032212"
     }, 
     {
       "lat": "4.83643281186151", 
       "lon": "52.3697324962106", 
       "name": "Jan Evertsenstraat, Amsterdam", 
       "id": "032222"
     }, 
     {
       "lat": "4.82751687090849", 
       "lon": "52.366482054151", 
       "name": "Hermitagelaan, Amsterdam", 
       "id": "032232"
     }, 
     {
       "lat": "4.82782223775004", 
       "lon": "52.3667171791707", 
       "name": "Hermitagelaan, Amsterdam", 
       "id": "032242"
     }, 
     {
       "lat": "4.7830812536594", 
       "lon": "52.3615630237793", 
       "name": "Jan Rebelstraat, Amsterdam", 
       "id": "040012"
     }, 
     {
       "lat": "4.78422115299119", 
       "lon": "52.3619463232368", 
       "name": "Jan Rebelstraat, Amsterdam", 
       "id": "040022"
     }, 
     {
       "lat": "4.78646721101757", 
       "lon": "52.3554505726125", 
       "name": "Dijkgraafplein, Amsterdam", 
       "id": "040081"
     }, 
     {
       "lat": "4.78689140960293", 
       "lon": "52.355560578486", 
       "name": "Dijkgraafplein, Amsterdam", 
       "id": "040091"
     }, 
     {
       "lat": "4.79172281252806", 
       "lon": "52.3565017392486", 
       "name": "Baden Powellweg, Amsterdam", 
       "id": "040111"
     }, 
     {
       "lat": "4.79137101835029", 
       "lon": "52.3564640177137", 
       "name": "Baden Powellweg, Amsterdam", 
       "id": "040121"
     }, 
     {
       "lat": "4.79927712607951", 
       "lon": "52.3580224886556", 
       "name": "Hoekenes, Amsterdam", 
       "id": "040151"
     }, 
     {
       "lat": "4.79854462070159", 
       "lon": "52.3579109946174", 
       "name": "Hoekenes, Amsterdam", 
       "id": "040161"
     }, 
     {
       "lat": "4.80062507394859", 
       "lon": "52.3582179196644", 
       "name": "Hoekenes, Amsterdam", 
       "id": "040192"
     }, 
     {
       "lat": "4.80028603529541", 
       "lon": "52.3583240926472", 
       "name": "Hoekenes, Amsterdam", 
       "id": "040202"
     }, 
     {
       "lat": "4.80322607172281", 
       "lon": "52.3591295592691", 
       "name": "Osdorpplein, Amsterdam", 
       "id": "040211"
     }, 
     {
       "lat": "4.80321956617863", 
       "lon": "52.359623855675", 
       "name": "Osdorpplein, Amsterdam", 
       "id": "040221"
     }, 
     {
       "lat": "4.78782539012926", 
       "lon": "52.3624859195266", 
       "name": "Baden Powellweg, Amsterdam", 
       "id": "040242"
     }, 
     {
       "lat": "4.78771074176196", 
       "lon": "52.3622786196622", 
       "name": "Baden Powellweg, Amsterdam", 
       "id": "040252"
     }, 
     {
       "lat": "4.7900166427771", 
       "lon": "52.3600253498951", 
       "name": "Saaftingestraat, Amsterdam", 
       "id": "040262"
     }, 
     {
       "lat": "4.7914062349491", 
       "lon": "52.3604008517974", 
       "name": "Saaftingestraat, Amsterdam", 
       "id": "040272"
     }, 
     {
       "lat": "4.79426117075254", 
       "lon": "52.3609814176879", 
       "name": "Reimerswaalstraat, Amsterdam", 
       "id": "040282"
     }, 
     {
       "lat": "4.79562410557206", 
       "lon": "52.3611590047893", 
       "name": "Reimerswaalstraat, Amsterdam", 
       "id": "040292"
     }, 
     {
       "lat": "4.79967956969264", 
       "lon": "52.3619970910047", 
       "name": "Bullepad, Amsterdam", 
       "id": "040302"
     }, 
     {
       "lat": "4.79934169064909", 
       "lon": "52.3620133891769", 
       "name": "Bullepad, Amsterdam", 
       "id": "040312"
     }, 
     {
       "lat": "4.80313353088457", 
       "lon": "52.3628140958172", 
       "name": "Geer Ban, Amsterdam", 
       "id": "040322"
     }, 
     {
       "lat": "4.80423431863329", 
       "lon": "52.3628374973715", 
       "name": "Geer Ban, Amsterdam", 
       "id": "040332"
     }, 
     {
       "lat": "4.80600419943512", 
       "lon": "52.3622170551416", 
       "name": "Vrijzicht, Amsterdam", 
       "id": "040382"
     }, 
     {
       "lat": "4.80620548441884", 
       "lon": "52.3625416034073", 
       "name": "Vrijzicht, Amsterdam", 
       "id": "040392"
     }, 
     {
       "lat": "4.80746434092143", 
       "lon": "52.359455977003", 
       "name": "Ruimzicht, Amsterdam", 
       "id": "040402"
     }, 
     {
       "lat": "4.8076502405035", 
       "lon": "52.3598343743691", 
       "name": "Ruimzicht, Amsterdam", 
       "id": "040412"
     }, 
     {
       "lat": "4.80758107024189", 
       "lon": "52.3595104753537", 
       "name": "Ruimzicht, Amsterdam", 
       "id": "040421"
     }, 
     {
       "lat": "4.80748947228086", 
       "lon": "52.3597796604314", 
       "name": "Ruimzicht, Amsterdam", 
       "id": "040431"
     }, 
     {
       "lat": "4.80563360731078", 
       "lon": "52.3580089503549", 
       "name": "Stadsdeel Osdorp, Amsterdam", 
       "id": "040442"
     }, 
     {
       "lat": "4.80688059451825", 
       "lon": "52.3580689970855", 
       "name": "Stadsdeel Osdorp, Amsterdam", 
       "id": "040462"
     }, 
     {
       "lat": "4.80881932626439", 
       "lon": "52.3568651342117", 
       "name": "Meer en Vaart, Amsterdam", 
       "id": "040472"
     }, 
     {
       "lat": "4.80918476343054", 
       "lon": "52.3569837605516", 
       "name": "Meer en Vaart, Amsterdam", 
       "id": "040482"
     }, 
     {
       "lat": "4.8105859850997", 
       "lon": "52.3564693027882", 
       "name": "Meer en Vaart, Amsterdam", 
       "id": "040491"
     }, 
     {
       "lat": "4.80994142892074", 
       "lon": "52.3563672954631", 
       "name": "Meer en Vaart, Amsterdam", 
       "id": "040501"
     }, 
     {
       "lat": "4.81137689220601", 
       "lon": "52.3543430461399", 
       "name": "C.K. Eloutstraat, Amsterdam", 
       "id": "040512"
     }, 
     {
       "lat": "4.81168348865664", 
       "lon": "52.3544703663998", 
       "name": "C.K. Eloutstraat, Amsterdam", 
       "id": "040522"
     }, 
     {
       "lat": "4.81537390112398", 
       "lon": "52.355135373434", 
       "name": "Piet Wiedijkstraat, Amsterdam", 
       "id": "040532"
     }, 
     {
       "lat": "4.8153435032066", 
       "lon": "52.3552161166885", 
       "name": "Piet Wiedijkstraat, Amsterdam", 
       "id": "040542"
     }, 
     {
       "lat": "4.82145901875887", 
       "lon": "52.3568003909099", 
       "name": "V. M. Broekmanstraat, Amsterdam", 
       "id": "040552"
     }, 
     {
       "lat": "4.82138998147658", 
       "lon": "52.3564585251628", 
       "name": "V. M. Broekmanstraat, Amsterdam", 
       "id": "040562"
     }, 
     {
       "lat": "4.82163450515074", 
       "lon": "52.3591560280645", 
       "name": "Hemsterhuisstraat, Amsterdam", 
       "id": "040572"
     }, 
     {
       "lat": "4.82182579209287", 
       "lon": "52.3591209907226", 
       "name": "Hemsterhuisstraat, Amsterdam", 
       "id": "040582"
     }, 
     {
       "lat": "4.83972031874826", 
       "lon": "52.3579647929689", 
       "name": "Derkinderenstraat, Amsterdam", 
       "id": "040601"
     }, 
     {
       "lat": "4.84014633599898", 
       "lon": "52.3579397992402", 
       "name": "Derkinderenstraat, Amsterdam", 
       "id": "040611"
     }, 
     {
       "lat": "4.82582066737917", 
       "lon": "52.3578098124743", 
       "name": "Johan Huizingalaan, Amsterdam", 
       "id": "040621"
     }, 
     {
       "lat": "4.82626136947786", 
       "lon": "52.3577849383522", 
       "name": "Johan Huizingalaan, Amsterdam", 
       "id": "040631"
     }, 
     {
       "lat": "4.81532945851386", 
       "lon": "52.3574450202609", 
       "name": "Piet Wiedijkstraat, Amsterdam", 
       "id": "040641"
     }, 
     {
       "lat": "4.81575455826043", 
       "lon": "52.3574920121647", 
       "name": "Piet Wiedijkstraat, Amsterdam", 
       "id": "040651"
     }, 
     {
       "lat": "4.79748812616442", 
       "lon": "52.356773273327", 
       "name": "Wolbrantskerkweg, Amsterdam", 
       "id": "040662"
     }, 
     {
       "lat": "4.79758991898942", 
       "lon": "52.3568456828131", 
       "name": "Wolbrantskerkweg, Amsterdam", 
       "id": "040672"
     }, 
     {
       "lat": "4.79968244380233", 
       "lon": "52.3529104426567", 
       "name": "Koos Vorrinkweg, Amsterdam", 
       "id": "040682"
     }, 
     {
       "lat": "4.79932754193577", 
       "lon": "52.3520009120553", 
       "name": "Koos Vorrinkweg, Amsterdam", 
       "id": "040692"
     }, 
     {
       "lat": "4.79621668471733", 
       "lon": "52.3486329660674", 
       "name": "J. v. Zutphenplantsoen, Amsterdam", 
       "id": "040722"
     }, 
     {
       "lat": "4.7961699053866", 
       "lon": "52.3488394522134", 
       "name": "J. v. Zutphenplantsoen, Amsterdam", 
       "id": "040732"
     }, 
     {
       "lat": "4.79933661920774", 
       "lon": "52.3446669013809", 
       "name": "Kortrijk, Amsterdam", 
       "id": "040742"
     }, 
     {
       "lat": "4.79923485138342", 
       "lon": "52.3445944932589", 
       "name": "Kortrijk, Amsterdam", 
       "id": "040752"
     }, 
     {
       "lat": "4.79734558609394", 
       "lon": "52.3432009671736", 
       "name": "Osdorperweg, Amsterdam", 
       "id": "040762"
     }, 
     {
       "lat": "4.797638704366", 
       "lon": "52.3432293912727", 
       "name": "Osdorperweg, Amsterdam", 
       "id": "040772"
     }, 
     {
       "lat": "4.81438708057393", 
       "lon": "52.341747763652", 
       "name": "Sloterweg, Amsterdam", 
       "id": "040842"
     }, 
     {
       "lat": "4.82436158069715", 
       "lon": "52.3466939763098", 
       "name": "Louwesweg, Amsterdam", 
       "id": "040881"
     }, 
     {
       "lat": "4.82436158069715", 
       "lon": "52.3466939763098", 
       "name": "Louwesweg, Amsterdam", 
       "id": "040882"
     }, 
     {
       "lat": "4.82513924346768", 
       "lon": "52.3467066598681", 
       "name": "Louwesweg, Amsterdam", 
       "id": "040891"
     }, 
     {
       "lat": "4.82513924346768", 
       "lon": "52.3467066598681", 
       "name": "Louwesweg, Amsterdam", 
       "id": "040892"
     }, 
     {
       "lat": "4.82311900027218", 
       "lon": "52.3463105728557", 
       "name": "Louweshoek, Amsterdam", 
       "id": "040912"
     }, 
     {
       "lat": "4.82754816039952", 
       "lon": "52.3477067331133", 
       "name": "Aletta Jacobslaan, Amsterdam", 
       "id": "040921"
     }, 
     {
       "lat": "4.82754895360771", 
       "lon": "52.3476438222974", 
       "name": "Aletta Jacobslaan, Amsterdam", 
       "id": "040922"
     }, 
     {
       "lat": "4.82749557853088", 
       "lon": "52.3472211434943", 
       "name": "Aletta Jacobslaan, Amsterdam", 
       "id": "040931"
     }, 
     {
       "lat": "4.82749557853088", 
       "lon": "52.3472211434943", 
       "name": "Aletta Jacobslaan, Amsterdam", 
       "id": "040932"
     }, 
     {
       "lat": "4.82846810190313", 
       "lon": "52.3469111658577", 
       "name": "Aletta Jacobslaan, Amsterdam", 
       "id": "040942"
     }, 
     {
       "lat": "4.82907034641623", 
       "lon": "52.3468690685159", 
       "name": "Aletta Jacobslaan, Amsterdam", 
       "id": "040952"
     }, 
     {
       "lat": "4.8337953938173", 
       "lon": "52.346918220235", 
       "name": "Ottho Heldringstraat, Amsterdam", 
       "id": "040962"
     }, 
     {
       "lat": "4.83304628949052", 
       "lon": "52.3469686418636", 
       "name": "Ottho Heldringstraat, Amsterdam", 
       "id": "040972"
     }, 
     {
       "lat": "4.83832923094439", 
       "lon": "52.3470022477769", 
       "name": "Maassluisstraat, Amsterdam", 
       "id": "040982"
     }, 
     {
       "lat": "4.83897538195964", 
       "lon": "52.3469692914465", 
       "name": "Maassluisstraat, Amsterdam", 
       "id": "040992"
     }, 
     {
       "lat": "4.84248395716341", 
       "lon": "52.3468866259813", 
       "name": "Naaldwijkstraat, Amsterdam", 
       "id": "041002"
     }, 
     {
       "lat": "4.8425872343993", 
       "lon": "52.3468421623351", 
       "name": "Naaldwijkstraat, Amsterdam", 
       "id": "041012"
     }, 
     {
       "lat": "4.84679768122858", 
       "lon": "52.346969315704", 
       "name": "Aalsmeerplein, Amsterdam", 
       "id": "041022"
     }, 
     {
       "lat": "4.84638710514289", 
       "lon": "52.3469404769386", 
       "name": "Aalsmeerplein, Amsterdam", 
       "id": "041032"
     }, 
     {
       "lat": "4.84949643034679", 
       "lon": "52.3507384989779", 
       "name": "Hoofddorpplein, Amsterdam", 
       "id": "041042"
     }, 
     {
       "lat": "4.84942381053094", 
       "lon": "52.3506752546199", 
       "name": "Hoofddorpplein, Amsterdam", 
       "id": "041052"
     }, 
     {
       "lat": "4.84503871982919", 
       "lon": "52.3515989660765", 
       "name": "Westlandgracht, Amsterdam", 
       "id": "041091"
     }, 
     {
       "lat": "4.84503871982919", 
       "lon": "52.3515989660765", 
       "name": "Westlandgracht, Amsterdam", 
       "id": "041092"
     }, 
     {
       "lat": "4.84581702308933", 
       "lon": "52.3515665774717", 
       "name": "Westlandgracht, Amsterdam", 
       "id": "041101"
     }, 
     {
       "lat": "4.84581702308933", 
       "lon": "52.3515665774717", 
       "name": "Westlandgracht, Amsterdam", 
       "id": "041102"
     }, 
     {
       "lat": "4.84191313769224", 
       "lon": "52.3515396690013", 
       "name": "Delflandlaan, Amsterdam", 
       "id": "041111"
     }, 
     {
       "lat": "4.84191313769224", 
       "lon": "52.3515396690013", 
       "name": "Delflandlaan, Amsterdam", 
       "id": "041112"
     }, 
     {
       "lat": "4.82742616485476", 
       "lon": "52.3492340811362", 
       "name": "Johan Huizingalaan, Amsterdam", 
       "id": "041121"
     }, 
     {
       "lat": "4.82742616485476", 
       "lon": "52.3492340811362", 
       "name": "Johan Huizingalaan, Amsterdam", 
       "id": "041122"
     }, 
     {
       "lat": "4.82750158416958", 
       "lon": "52.3490726575471", 
       "name": "Johan Huizingalaan, Amsterdam", 
       "id": "041131"
     }, 
     {
       "lat": "4.82750158416958", 
       "lon": "52.3490726575471", 
       "name": "Johan Huizingalaan, Amsterdam", 
       "id": "041132"
     }, 
     {
       "lat": "4.83372345392564", 
       "lon": "52.3515106436851", 
       "name": "Heemstedestraat, Amsterdam", 
       "id": "041141"
     }, 
     {
       "lat": "4.83416408912117", 
       "lon": "52.3514857400074", 
       "name": "Heemstedestraat, Amsterdam", 
       "id": "041161"
     }, 
     {
       "lat": "4.78598315214223", 
       "lon": "52.3565086763866", 
       "name": "Wierdestraat, Amsterdam", 
       "id": "041172"
     }, 
     {
       "lat": "4.83969662908039", 
       "lon": "52.3515564001825", 
       "name": "Delflandlaan, Amsterdam", 
       "id": "041201"
     }, 
     {
       "lat": "4.83926220581944", 
       "lon": "52.3641552423144", 
       "name": "Derkinderenstraat, Amsterdam", 
       "id": "041292"
     }, 
     {
       "lat": "4.83963033593709", 
       "lon": "52.3640670680353", 
       "name": "Derkinderenstraat, Amsterdam", 
       "id": "041302"
     }, 
     {
       "lat": "4.83575482817207", 
       "lon": "52.3640311035061", 
       "name": "Jan Tooropstraat, Amsterdam", 
       "id": "041312"
     }, 
     {
       "lat": "4.83537212166345", 
       "lon": "52.3641102100503", 
       "name": "Jan Tooropstraat, Amsterdam", 
       "id": "041322"
     }, 
     {
       "lat": "4.82910398475484", 
       "lon": "52.3640358874296", 
       "name": "Robert Fruinlaan, Amsterdam", 
       "id": "041332"
     }, 
     {
       "lat": "4.83010295470922", 
       "lon": "52.3639866660632", 
       "name": "Robert Fruinlaan, Amsterdam", 
       "id": "041342"
     }, 
     {
       "lat": "4.82725660578368", 
       "lon": "52.3615105887948", 
       "name": "Justus Lipsiusstraat, Amsterdam", 
       "id": "041352"
     }, 
     {
       "lat": "4.82704514341596", 
       "lon": "52.3608175299737", 
       "name": "Justus Lipsiusstraat, Amsterdam", 
       "id": "041362"
     }, 
     {
       "lat": "4.82677705362958", 
       "lon": "52.3576345887222", 
       "name": "Cornelis Lelylaan, Amsterdam", 
       "id": "041382"
     }, 
     {
       "lat": "4.82771218148467", 
       "lon": "52.357980547856", 
       "name": "Cornelis Lelylaan, Amsterdam", 
       "id": "041392"
     }, 
     {
       "lat": "4.82732369048673", 
       "lon": "52.3550307193128", 
       "name": "Pieter Calandlaan, Amsterdam", 
       "id": "041402"
     }, 
     {
       "lat": "4.82738387550582", 
       "lon": "52.3549141628038", 
       "name": "Pieter Calandlaan, Amsterdam", 
       "id": "041412"
     }, 
     {
       "lat": "4.8404352830011", 
       "lon": "52.3630821350575", 
       "name": "M. Bauerstraat, Amsterdam", 
       "id": "041592"
     }, 
     {
       "lat": "4.84056275668992", 
       "lon": "52.3634602096021", 
       "name": "M. Bauerstraat, Amsterdam", 
       "id": "041602"
     }, 
     {
       "lat": "4.84053103749781", 
       "lon": "52.3588852920635", 
       "name": "J. Jongkindstraat, Amsterdam", 
       "id": "041612"
     }, 
     {
       "lat": "4.8407059690671", 
       "lon": "52.3589849652177", 
       "name": "J. Jongkindstraat, Amsterdam", 
       "id": "041622"
     }, 
     {
       "lat": "4.79303678050558", 
       "lon": "52.341687432786", 
       "name": "Langsom, Amsterdam", 
       "id": "041672"
     }, 
     {
       "lat": "4.79356369764365", 
       "lon": "52.3417889433052", 
       "name": "Langsom, Amsterdam", 
       "id": "041682"
     }, 
     {
       "lat": "4.82792491968995", 
       "lon": "52.3434303218846", 
       "name": "Henk Sneevlietweg, Amsterdam", 
       "id": "041692"
     }, 
     {
       "lat": "4.82753331272084", 
       "lon": "52.344228384964", 
       "name": "Henk Sneevlietweg, Amsterdam", 
       "id": "041712"
     }, 
     {
       "lat": "4.80083770190707", 
       "lon": "52.3521252446369", 
       "name": "Koos Vorrinkweg, Amsterdam", 
       "id": "041822"
     }, 
     {
       "lat": "4.80491943591112", 
       "lon": "52.3531430414746", 
       "name": "De La Sallestraat, Amsterdam", 
       "id": "041832"
     }, 
     {
       "lat": "4.8059172448198", 
       "lon": "52.3531659215931", 
       "name": "De La Sallestraat, Amsterdam", 
       "id": "041842"
     }, 
     {
       "lat": "4.80334078457434", 
       "lon": "52.3593368443265", 
       "name": "Osdorpplein, Amsterdam", 
       "id": "041852"
     }, 
     {
       "lat": "4.8030925401462", 
       "lon": "52.3592367539327", 
       "name": "Osdorpplein, Amsterdam", 
       "id": "041862"
     }, 
     {
       "lat": "4.84001982870151", 
       "lon": "52.3562944526069", 
       "name": "Kon. Wilhelminaplein, Amsterdam", 
       "id": "041882"
     }, 
     {
       "lat": "4.83894731834055", 
       "lon": "52.356370379883", 
       "name": "Kon. Wilhelminaplein, Amsterdam", 
       "id": "041892"
     }, 
     {
       "lat": "4.83429184951798", 
       "lon": "52.3565464566951", 
       "name": "Station Lelylaan, Amsterdam", 
       "id": "041902"
     }, 
     {
       "lat": "4.83144786063656", 
       "lon": "52.3562455293442", 
       "name": "R. Engelmanstraat, Amsterdam", 
       "id": "041912"
     }, 
     {
       "lat": "4.83061018869276", 
       "lon": "52.356322483451", 
       "name": "R. Engelmanstraat, Amsterdam", 
       "id": "041922"
     }, 
     {
       "lat": "4.83459820852848", 
       "lon": "52.3578780777765", 
       "name": "Station Lelylaan, Amsterdam", 
       "id": "041951"
     }, 
     {
       "lat": "4.83381989869294", 
       "lon": "52.3579014051323", 
       "name": "Station Lelylaan, Amsterdam", 
       "id": "041961"
     }, 
     {
       "lat": "4.80801032774804", 
       "lon": "52.3536165844735", 
       "name": "Louis Davidsstraat, Amsterdam", 
       "id": "042002"
     }, 
     {
       "lat": "4.80768601921113", 
       "lon": "52.3537228506522", 
       "name": "Louis Davidsstraat, Amsterdam", 
       "id": "042012"
     }, 
     {
       "lat": "4.82255581355985", 
       "lon": "52.3421285580363", 
       "name": "Sloterweg 700, Amsterdam", 
       "id": "042052"
     }, 
     {
       "lat": "4.83096379593822", 
       "lon": "52.3515336579548", 
       "name": "Jac. Veltmanstraat, Amsterdam", 
       "id": "042082"
     }, 
     {
       "lat": "4.77942575810924", 
       "lon": "52.3583446526796", 
       "name": "Griendstraat, Amsterdam", 
       "id": "042142"
     }, 
     {
       "lat": "4.7799165958259", 
       "lon": "52.3589493550784", 
       "name": "Griendstraat, Amsterdam", 
       "id": "042152"
     }, 
     {
       "lat": "4.7761003353213", 
       "lon": "52.35571207741", 
       "name": "M. Gandhilaan, Amsterdam", 
       "id": "042182"
     }, 
     {
       "lat": "4.77695174812452", 
       "lon": "52.3567770322764", 
       "name": "Baldwinstraat, Amsterdam", 
       "id": "042192"
     }, 
     {
       "lat": "4.7771260338722", 
       "lon": "52.3569127479028", 
       "name": "Baldwinstraat, Amsterdam", 
       "id": "042202"
     }, 
     {
       "lat": "4.82036830701148", 
       "lon": "52.3514024997404", 
       "name": "Aarschotpad, Amsterdam", 
       "id": "042212"
     }, 
     {
       "lat": "4.82048709672849", 
       "lon": "52.3512952150522", 
       "name": "Aarschotpad, Amsterdam", 
       "id": "042222"
     }, 
     {
       "lat": "4.82753370588285", 
       "lon": "52.3407051674501", 
       "name": "IBM, Amsterdam", 
       "id": "042262"
     }, 
     {
       "lat": "4.78115117540669", 
       "lon": "52.3599173777485", 
       "name": "Zuidermolenweg, Amsterdam", 
       "id": "042292"
     }, 
     {
       "lat": "4.82512454522093", 
       "lon": "52.3513442919997", 
       "name": "Johan Huizingalaan, Amsterdam", 
       "id": "042302"
     }, 
     {
       "lat": "4.82626795462466", 
       "lon": "52.351457569861", 
       "name": "Johan Huizingalaan, Amsterdam", 
       "id": "042312"
     }, 
     {
       "lat": "4.8160892464072", 
       "lon": "52.3485957119826", 
       "name": "Maaseikpad, Amsterdam", 
       "id": "042342"
     }, 
     {
       "lat": "4.81591892241521", 
       "lon": "52.3481454998761", 
       "name": "Maaseikpad, Amsterdam", 
       "id": "042352"
     }, 
     {
       "lat": "4.79541963046", 
       "lon": "52.3236517820217", 
       "name": "Hotel Ibis, Badhoevedorp", 
       "id": "042382"
     }, 
     {
       "lat": "4.7953895772904", 
       "lon": "52.3237055588466", 
       "name": "Hotel Ibis, Badhoevedorp", 
       "id": "042392"
     }, 
     {
       "lat": "4.78423408148803", 
       "lon": "52.3285835655897", 
       "name": "Schuilhoeve, Badhoevedorp", 
       "id": "042402"
     }, 
     {
       "lat": "4.78298990666557", 
       "lon": "52.3294580285433", 
       "name": "Schuilhoeve, Badhoevedorp", 
       "id": "042412"
     }, 
     {
       "lat": "4.77879849778791", 
       "lon": "52.3323576039044", 
       "name": "PA Verkuyllaan, Badhoevedorp", 
       "id": "042422"
     }, 
     {
       "lat": "4.77908043142946", 
       "lon": "52.3321253689941", 
       "name": "PA Verkuyllaan, Badhoevedorp", 
       "id": "042432"
     }, 
     {
       "lat": "4.77981061997616", 
       "lon": "52.3355894430634", 
       "name": "R.K. Kerk, Badhoevedorp", 
       "id": "042442"
     }, 
     {
       "lat": "4.78017617289356", 
       "lon": "52.3356811974328", 
       "name": "R.K. Kerk, Badhoevedorp", 
       "id": "042452"
     }, 
     {
       "lat": "4.79011710867929", 
       "lon": "52.3405582462567", 
       "name": "Badhoevelaan, Badhoevedorp", 
       "id": "042482"
     }, 
     {
       "lat": "4.78976749821645", 
       "lon": "52.3403677372199", 
       "name": "Badhoevelaan, Badhoevedorp", 
       "id": "042492"
     }, 
     {
       "lat": "4.79320263031625", 
       "lon": "52.3391626846269", 
       "name": "Nieuwe Meerdijk 69, Badhoevedorp", 
       "id": "042512"
     }, 
     {
       "lat": "4.79289439706733", 
       "lon": "52.336977092795", 
       "name": "Uiverstraat, Schiphol", 
       "id": "042522"
     }, 
     {
       "lat": "4.79016359081691", 
       "lon": "52.3360106348469", 
       "name": "Rijstvogelstraat, Badhoevedorp", 
       "id": "042542"
     }, 
     {
       "lat": "4.78908790074809", 
       "lon": "52.3385307856092", 
       "name": "Spechtstraat, Amsterdam", 
       "id": "042562"
     }, 
     {
       "lat": "4.78478978608028", 
       "lon": "52.338446067887", 
       "name": "Badhoevedorp, Havikstraat, badhoevedorp", 
       "id": "042582"
     }, 
     {
       "lat": "4.7848625375311", 
       "lon": "52.3384913774358", 
       "name": "Badhoevedorp, Havikstraat, badhoevedorp", 
       "id": "042592"
     }, 
     {
       "lat": "4.82796959567019", 
       "lon": "52.3410487647778", 
       "name": "IBM, Amsterdam", 
       "id": "042752"
     }, 
     {
       "lat": "4.81567675052774", 
       "lon": "52.3464366479298", 
       "name": "Laan v.Vlaanderen, Amsterdam", 
       "id": "042761"
     }, 
     {
       "lat": "4.81642459396374", 
       "lon": "52.3464851960067", 
       "name": "Laan v.Vlaanderen, Amsterdam", 
       "id": "042771"
     }, 
     {
       "lat": "4.81061530542694", 
       "lon": "52.3463042436897", 
       "name": "Kasterleepark, Amsterdam", 
       "id": "042781"
     }, 
     {
       "lat": "4.81103982681724", 
       "lon": "52.3463872014324", 
       "name": "Kasterleepark, Amsterdam", 
       "id": "042791"
     }, 
     {
       "lat": "4.80528698226415", 
       "lon": "52.3475005070622", 
       "name": "Westmallepad, Amsterdam", 
       "id": "043052"
     }, 
     {
       "lat": "4.80535169160179", 
       "lon": "52.3470424468429", 
       "name": "Westmallepad, Amsterdam", 
       "id": "043062"
     }, 
     {
       "lat": "4.81591895198402", 
       "lon": "52.3458625977257", 
       "name": "Antwerpenbaan, Amsterdam", 
       "id": "043072"
     }, 
     {
       "lat": "4.81623959979178", 
       "lon": "52.3460349134048", 
       "name": "Antwerpenbaan, Amsterdam", 
       "id": "043082"
     }, 
     {
       "lat": "4.82490061696848", 
       "lon": "52.3423734055104", 
       "name": "L. Armstrongstraat, Amsterdam", 
       "id": "043132"
     }, 
     {
       "lat": "4.80382353411853", 
       "lon": "52.3449497510906", 
       "name": "Oudenaardeplantsoen, Amsterdam", 
       "id": "043141"
     }, 
     {
       "lat": "4.8126271422286", 
       "lon": "52.3450737104197", 
       "name": "Hageland, Amsterdam", 
       "id": "043152"
     }, 
     {
       "lat": "4.81229137542204", 
       "lon": "52.3449372626438", 
       "name": "Hageland, Amsterdam", 
       "id": "043162"
     }, 
     {
       "lat": "4.8345453916251", 
       "lon": "52.346795895704", 
       "name": "Henk Sneevlietweg, Amsterdam", 
       "id": "043183"
     }, 
     {
       "lat": "4.83439056939381", 
       "lon": "52.3462648928747", 
       "name": "Henk Sneevlietweg, Amsterdam", 
       "id": "043193"
     }, 
     {
       "lat": "4.83434963467908", 
       "lon": "52.3530864320959", 
       "name": "Heemstedestraat, Amsterdam", 
       "id": "043203"
     }, 
     {
       "lat": "4.83420947011003", 
       "lon": "52.3525554982205", 
       "name": "Heemstedestraat, Amsterdam", 
       "id": "043213"
     }, 
     {
       "lat": "4.83446240548335", 
       "lon": "52.3581740402047", 
       "name": "Station Lelylaan, Amsterdam", 
       "id": "043223"
     }, 
     {
       "lat": "4.83426328506064", 
       "lon": "52.3576608072269", 
       "name": "Station Lelylaan, Amsterdam", 
       "id": "043233"
     }, 
     {
       "lat": "4.83402428976339", 
       "lon": "52.3650566223169", 
       "name": "Postjesweg, Amsterdam", 
       "id": "043243"
     }, 
     {
       "lat": "4.83385282430649", 
       "lon": "52.3646783350704", 
       "name": "Postjesweg, Amsterdam", 
       "id": "043253"
     }, 
     {
       "lat": "4.81016277016185", 
       "lon": "52.3506341604396", 
       "name": "Plesmanlaan, Amsterdam", 
       "id": "043262"
     }, 
     {
       "lat": "4.81044232064855", 
       "lon": "52.3505815962161", 
       "name": "Plesmanlaan, Amsterdam", 
       "id": "043272"
     }, 
     {
       "lat": "4.82231894440348", 
       "lon": "52.3561304140247", 
       "name": "L. Bouwmeesterstraat, Amsterdam", 
       "id": "043282"
     }, 
     {
       "lat": "4.82217170522156", 
       "lon": "52.3561656624091", 
       "name": "L. Bouwmeesterstraat, Amsterdam", 
       "id": "043292"
     }, 
     {
       "lat": "4.81443518759941", 
       "lon": "52.3357441327359", 
       "name": "Anderlechtlaan, Amsterdam", 
       "id": "043322"
     }, 
     {
       "lat": "4.81481525345401", 
       "lon": "52.3358538257058", 
       "name": "Anderlechtlaan, Amsterdam", 
       "id": "043332"
     }, 
     {
       "lat": "4.80733177596704", 
       "lon": "52.3448861023135", 
       "name": "Brusselsingel, Amsterdam", 
       "id": "043382"
     }, 
     {
       "lat": "4.80740350454157", 
       "lon": "52.3450122831384", 
       "name": "Brusselsingel, Amsterdam", 
       "id": "043392"
     }, 
     {
       "lat": "4.80415998314699", 
       "lon": "52.3450322994519", 
       "name": "Oudenaardeplantsoen, Amsterdam", 
       "id": "043401"
     }, 
     {
       "lat": "4.7916921294267", 
       "lon": "52.3566004507305", 
       "name": "Baden Powellweg, Amsterdam", 
       "id": "043432"
     }, 
     {
       "lat": "4.83386169598191", 
       "lon": "52.3569039576535", 
       "name": "Station Lelylaan, Amsterdam", 
       "id": "043442"
     }, 
     {
       "lat": "4.74083767384501", 
       "lon": "52.2965012541162", 
       "name": "Toekanweg, Schiphol", 
       "id": "043752"
     }, 
     {
       "lat": "4.74467201558349", 
       "lon": "52.29796022143", 
       "name": "Pelikaanweg, Schiphol", 
       "id": "043812"
     }, 
     {
       "lat": "4.77381861834874", 
       "lon": "52.3529949411049", 
       "name": "La Meye, Amsterdam", 
       "id": "043832"
     }, 
     {
       "lat": "4.83874186838493", 
       "lon": "52.3516148943538", 
       "name": "Delflandlaan, Amsterdam", 
       "id": "043872"
     }, 
     {
       "lat": "4.83535356703995", 
       "lon": "52.3514373651284", 
       "name": "Heemstedestraat, Amsterdam", 
       "id": "043892"
     }, 
     {
       "lat": "4.77680006201614", 
       "lon": "52.3517969984545", 
       "name": "Presanella, Amsterdam", 
       "id": "043902"
     }, 
     {
       "lat": "4.7815083982225", 
       "lon": "52.3498798174273", 
       "name": "Allenstraat, Amsterdam", 
       "id": "043922"
     }, 
     {
       "lat": "4.78712362263906", 
       "lon": "52.3492433221336", 
       "name": "Ecuplein, Amsterdam", 
       "id": "043942"
     }, 
     {
       "lat": "4.77437836299565", 
       "lon": "52.3539145984469", 
       "name": "Matterhorn, Amsterdam", 
       "id": "044011"
     }, 
     {
       "lat": "4.77477737894061", 
       "lon": "52.3537189316343", 
       "name": "Matterhorn, Amsterdam", 
       "id": "044021"
     }, 
     {
       "lat": "4.77696110510943", 
       "lon": "52.3528943432082", 
       "name": "Pilatus, Amsterdam", 
       "id": "044031"
     }, 
     {
       "lat": "4.77668125344894", 
       "lon": "52.3529648025859", 
       "name": "Pilatus, Amsterdam", 
       "id": "044041"
     }, 
     {
       "lat": "4.78342532956852", 
       "lon": "52.3503030518355", 
       "name": "Inaristraat, Amsterdam", 
       "id": "044051"
     }, 
     {
       "lat": "4.78314562678954", 
       "lon": "52.3503645393811", 
       "name": "Inaristraat, Amsterdam", 
       "id": "044061"
     }, 
     {
       "lat": "4.78817409378028", 
       "lon": "52.3497070223759", 
       "name": "Ecuplein, Amsterdam", 
       "id": "044071"
     }, 
     {
       "lat": "4.78886253067798", 
       "lon": "52.3498093707633", 
       "name": "Ecuplein, Amsterdam", 
       "id": "044081"
     }, 
     {
       "lat": "4.79441020829649", 
       "lon": "52.3509248122609", 
       "name": "Baden Powellweg, Amsterdam", 
       "id": "044091"
     }, 
     {
       "lat": "4.79441020829649", 
       "lon": "52.3509248122609", 
       "name": "Baden Powellweg, Amsterdam", 
       "id": "044092"
     }, 
     {
       "lat": "4.79518637736188", 
       "lon": "52.3510545265204", 
       "name": "Baden Powellweg, Amsterdam", 
       "id": "044101"
     }, 
     {
       "lat": "4.79518637736188", 
       "lon": "52.3510545265204", 
       "name": "Baden Powellweg, Amsterdam", 
       "id": "044102"
     }, 
     {
       "lat": "4.80183169242404", 
       "lon": "52.3524357501288", 
       "name": "Hoekenes, Amsterdam", 
       "id": "044111"
     }, 
     {
       "lat": "4.80260802817382", 
       "lon": "52.3525564285196", 
       "name": "Hoekenes, Amsterdam", 
       "id": "044121"
     }, 
     {
       "lat": "4.80850654281446", 
       "lon": "52.3538347187218", 
       "name": "Louis Davidsstraat, Amsterdam", 
       "id": "044131"
     }, 
     {
       "lat": "4.80910714378832", 
       "lon": "52.3539275315832", 
       "name": "Louis Davidsstraat, Amsterdam", 
       "id": "044141"
     }, 
     {
       "lat": "4.77457702168157", 
       "lon": "52.3544099569908", 
       "name": "Matterhorn, Amsterdam", 
       "id": "044162"
     }, 
     {
       "lat": "4.77511252670995", 
       "lon": "52.3549609844534", 
       "name": "Matterhorn, Amsterdam", 
       "id": "044172"
     }, 
     {
       "lat": "4.8113756424553", 
       "lon": "52.3340755231436", 
       "name": "Oude Haagseweg, Amsterdam", 
       "id": "044182"
     }, 
     {
       "lat": "4.80966768868846", 
       "lon": "52.3334110874441", 
       "name": "Oude Haagseweg, Amsterdam", 
       "id": "044192"
     }, 
     {
       "lat": "4.80272446625593", 
       "lon": "52.3292246117337", 
       "name": "Koekoekslaan, Schiphol", 
       "id": "044202"
     }, 
     {
       "lat": "4.80249023222755", 
       "lon": "52.3291875030192", 
       "name": "Koekoekslaan, Schiphol", 
       "id": "044212"
     }, 
     {
       "lat": "4.79893798659552", 
       "lon": "52.3481701692396", 
       "name": "Vrije Geer, Amsterdam", 
       "id": "044252"
     }, 
     {
       "lat": "4.79739588265568", 
       "lon": "52.3471468710276", 
       "name": "Vrije Geer, Amsterdam", 
       "id": "044262"
     }, 
     {
       "lat": "4.8033426539998", 
       "lon": "52.3491536761012", 
       "name": "Vlimmerenstraat, Amsterdam", 
       "id": "044272"
     }, 
     {
       "lat": "4.8224884568791", 
       "lon": "52.3370411344606", 
       "name": "Adam Smithplein, Amsterdam", 
       "id": "044282"
     }, 
     {
       "lat": "4.82094424694242", 
       "lon": "52.3373213652161", 
       "name": "Adam Smithplein, Amsterdam", 
       "id": "044292"
     }, 
     {
       "lat": "4.8056822371872", 
       "lon": "52.3666194862382", 
       "name": "Oeverpad, Amsterdam", 
       "id": "044312"
     }, 
     {
       "lat": "4.80496986151933", 
       "lon": "52.364962233731", 
       "name": "Oeverpad, Amsterdam", 
       "id": "044322"
     }, 
     {
       "lat": "4.80484351293211", 
       "lon": "52.3645212110374", 
       "name": "Oeverpad, Amsterdam", 
       "id": "044332"
     }, 
     {
       "lat": "4.90301331313286", 
       "lon": "52.3772945470558", 
       "name": "Centraal Station, Amsterdam", 
       "id": "050011"
     }, 
     {
       "lat": "4.90187979104669", 
       "lon": "52.3775415622275", 
       "name": "Centraal Station, Amsterdam", 
       "id": "050032"
     }, 
     {
       "lat": "4.90188175798516", 
       "lon": "52.3773618163898", 
       "name": "Centraal Station, Amsterdam", 
       "id": "050052"
     }, 
     {
       "lat": "4.90188087286512", 
       "lon": "52.3774427020176", 
       "name": "Centraal Station, Amsterdam", 
       "id": "050062"
     }, 
     {
       "lat": "4.90177630477286", 
       "lon": "52.3776040519113", 
       "name": "Centraal Station, Amsterdam", 
       "id": "050072"
     }, 
     {
       "lat": "4.89807439456932", 
       "lon": "52.3776966710244", 
       "name": "Centraal Station, Amsterdam", 
       "id": "050081"
     }, 
     {
       "lat": "4.89921540827245", 
       "lon": "52.3781058249021", 
       "name": "Centraal Station, Amsterdam", 
       "id": "050111"
     }, 
     {
       "lat": "4.90370545896632", 
       "lon": "52.3676895207105", 
       "name": "Mr. Visserplein, Amsterdam", 
       "id": "050132"
     }, 
     {
       "lat": "4.89673513831544", 
       "lon": "52.3779517747375", 
       "name": "Martelaarsgracht, Amsterdam", 
       "id": "050141"
     }, 
     {
       "lat": "4.90129483732286", 
       "lon": "52.3773144709877", 
       "name": "Centraal Station, Amsterdam", 
       "id": "050152"
     }, 
     {
       "lat": "4.90188028278303", 
       "lon": "52.3774966257687", 
       "name": "Centraal Station, Amsterdam", 
       "id": "050192"
     }, 
     {
       "lat": "4.90104075381549", 
       "lon": "52.3777178743938", 
       "name": "Centraal Station, Amsterdam", 
       "id": "050221"
     }, 
     {
       "lat": "4.90204585271139", 
       "lon": "52.3771288087351", 
       "name": "Centraal Station, Amsterdam", 
       "id": "050242"
     }, 
     {
       "lat": "4.89751059271696", 
       "lon": "52.378215627244", 
       "name": "Centraal Station, Amsterdam", 
       "id": "050252"
     }, 
     {
       "lat": "4.89790968195789", 
       "lon": "52.3779835968381", 
       "name": "Centraal Station, Amsterdam", 
       "id": "050262"
     }, 
     {
       "lat": "4.89776669482427", 
       "lon": "52.3776324857611", 
       "name": "Centraal Station, Amsterdam", 
       "id": "050302"
     }, 
     {
       "lat": "4.89348132422171", 
       "lon": "52.3734084506755", 
       "name": "Dam, Amsterdam", 
       "id": "050311"
     }, 
     {
       "lat": "4.89348132422171", 
       "lon": "52.3734084506755", 
       "name": "Dam, Amsterdam", 
       "id": "050312"
     }, 
     {
       "lat": "4.89420983060758", 
       "lon": "52.37392378534", 
       "name": "Dam, Amsterdam", 
       "id": "050321"
     }, 
     {
       "lat": "4.89780995766728", 
       "lon": "52.3777045661428", 
       "name": "Centraal Station, Amsterdam", 
       "id": "050332"
     }, 
     {
       "lat": "4.89781055270347", 
       "lon": "52.3776506424204", 
       "name": "Centraal Station, Amsterdam", 
       "id": "050342"
     }, 
     {
       "lat": "4.89210171720737", 
       "lon": "52.3693941706722", 
       "name": "Spui, Amsterdam", 
       "id": "050351"
     }, 
     {
       "lat": "4.89210171720737", 
       "lon": "52.3693941706722", 
       "name": "Spui, Amsterdam", 
       "id": "050352"
     }, 
     {
       "lat": "4.89209475815103", 
       "lon": "52.3687020874393", 
       "name": "Spui, Amsterdam", 
       "id": "050361"
     }, 
     {
       "lat": "4.89209475815103", 
       "lon": "52.3687020874393", 
       "name": "Spui, Amsterdam", 
       "id": "050362"
     }, 
     {
       "lat": "4.89329624343403", 
       "lon": "52.3676106041488", 
       "name": "Muntplein, Amsterdam", 
       "id": "050391"
     }, 
     {
       "lat": "4.89329624343403", 
       "lon": "52.3676106041488", 
       "name": "Muntplein, Amsterdam", 
       "id": "050392"
     }, 
     {
       "lat": "4.89286625698576", 
       "lon": "52.3679862937684", 
       "name": "Muntplein, Amsterdam", 
       "id": "050401"
     }, 
     {
       "lat": "4.89286625698576", 
       "lon": "52.3679862937684", 
       "name": "Muntplein, Amsterdam", 
       "id": "050402"
     }, 
     {
       "lat": "4.89627714177903", 
       "lon": "52.3662568687979", 
       "name": "Rembrandtplein, Amsterdam", 
       "id": "050461"
     }, 
     {
       "lat": "4.89627714177903", 
       "lon": "52.3662568687979", 
       "name": "Rembrandtplein, Amsterdam", 
       "id": "050462"
     }, 
     {
       "lat": "4.89702620330079", 
       "lon": "52.3662330092872", 
       "name": "Rembrandtplein, Amsterdam", 
       "id": "050471"
     }, 
     {
       "lat": "4.89702620330079", 
       "lon": "52.3662330092872", 
       "name": "Rembrandtplein, Amsterdam", 
       "id": "050472"
     }, 
     {
       "lat": "4.90611371808508", 
       "lon": "52.3676633799318", 
       "name": "Mr. Visserplein, Amsterdam", 
       "id": "050481"
     }, 
     {
       "lat": "4.90611371808508", 
       "lon": "52.3676633799318", 
       "name": "Mr. Visserplein, Amsterdam", 
       "id": "050482"
     }, 
     {
       "lat": "4.90234453978061", 
       "lon": "52.3672705205336", 
       "name": "Waterlooplein, Amsterdam", 
       "id": "050521"
     }, 
     {
       "lat": "4.90195156681441", 
       "lon": "52.3669543405943", 
       "name": "Waterlooplein, Amsterdam", 
       "id": "050531"
     }, 
     {
       "lat": "4.90195156681441", 
       "lon": "52.3669543405943", 
       "name": "Waterlooplein, Amsterdam", 
       "id": "050532"
     }, 
     {
       "lat": "4.8900776589802", 
       "lon": "52.3731245782283", 
       "name": "Dam, Amsterdam", 
       "id": "050552"
     }, 
     {
       "lat": "4.90539126835442", 
       "lon": "52.3679390611962", 
       "name": "Mr. Visserplein, Amsterdam", 
       "id": "050561"
     }, 
     {
       "lat": "4.90539126835442", 
       "lon": "52.3679390611962", 
       "name": "Mr. Visserplein, Amsterdam", 
       "id": "050562"
     }, 
     {
       "lat": "4.88932729867699", 
       "lon": "52.3693286103097", 
       "name": "Spui, Amsterdam", 
       "id": "050611"
     }, 
     {
       "lat": "4.88925650838999", 
       "lon": "52.369094631959", 
       "name": "Spui, Amsterdam", 
       "id": "050621"
     }, 
     {
       "lat": "4.89064329376082", 
       "lon": "52.3724438857075", 
       "name": "Dam, Amsterdam", 
       "id": "050631"
     }, 
     {
       "lat": "4.8907910346769", 
       "lon": "52.3736758214006", 
       "name": "Dam, Amsterdam", 
       "id": "050651"
     }, 
     {
       "lat": "4.89026794557149", 
       "lon": "52.3731793032443", 
       "name": "Dam, Amsterdam", 
       "id": "050661"
     }, 
     {
       "lat": "4.89123860384906", 
       "lon": "52.374360762711", 
       "name": "Dam, Amsterdam", 
       "id": "050682"
     }, 
     {
       "lat": "4.89372832390647", 
       "lon": "52.3762855457662", 
       "name": "Nieuwezijds Kolk, Amsterdam", 
       "id": "050691"
     }, 
     {
       "lat": "4.89372832390647", 
       "lon": "52.3762855457662", 
       "name": "Nieuwezijds Kolk, Amsterdam", 
       "id": "050692"
     }, 
     {
       "lat": "4.89283845215684", 
       "lon": "52.3757515594911", 
       "name": "Nieuwezijds Kolk, Amsterdam", 
       "id": "050701"
     }, 
     {
       "lat": "4.89283845215684", 
       "lon": "52.3757515594911", 
       "name": "Nieuwezijds Kolk, Amsterdam", 
       "id": "050702"
     }, 
     {
       "lat": "4.88453164645823", 
       "lon": "52.3739999347993", 
       "name": "Westermarkt, Amsterdam", 
       "id": "050731"
     }, 
     {
       "lat": "4.88453164645823", 
       "lon": "52.3739999347993", 
       "name": "Westermarkt, Amsterdam", 
       "id": "050732"
     }, 
     {
       "lat": "4.88354688795782", 
       "lon": "52.374076639556", 
       "name": "Westermarkt, Amsterdam", 
       "id": "050741"
     }, 
     {
       "lat": "4.88354688795782", 
       "lon": "52.374076639556", 
       "name": "Westermarkt, Amsterdam", 
       "id": "050742"
     }, 
     {
       "lat": "4.87615166678142", 
       "lon": "52.3722833596558", 
       "name": "Marnixstraat, Amsterdam", 
       "id": "050771"
     }, 
     {
       "lat": "4.87615166678142", 
       "lon": "52.3722833596558", 
       "name": "Marnixstraat, Amsterdam", 
       "id": "050772"
     }, 
     {
       "lat": "4.87701582829419", 
       "lon": "52.3724758284735", 
       "name": "Marnixstraat, Amsterdam", 
       "id": "050781"
     }, 
     {
       "lat": "4.87701582829419", 
       "lon": "52.3724758284735", 
       "name": "Marnixstraat, Amsterdam", 
       "id": "050782"
     }, 
     {
       "lat": "4.88805618360024", 
       "lon": "52.3831193860783", 
       "name": "Buiten Oranjestraat, Amsterdam", 
       "id": "050792"
     }, 
     {
       "lat": "4.88781906277658", 
       "lon": "52.3833071279548", 
       "name": "Buiten Oranjestraat, Amsterdam", 
       "id": "050802"
     }, 
     {
       "lat": "4.89156992251536", 
       "lon": "52.381507371604", 
       "name": "Buiten Brouwersstraat, Amsterdam", 
       "id": "050812"
     }, 
     {
       "lat": "4.89128906648747", 
       "lon": "52.3816679742909", 
       "name": "Buiten Brouwersstraat, Amsterdam", 
       "id": "050822"
     }, 
     {
       "lat": "4.89468318684659", 
       "lon": "52.3802261328124", 
       "name": "Singel, Amsterdam", 
       "id": "050842"
     }, 
     {
       "lat": "4.89611951133264", 
       "lon": "52.3818229193341", 
       "name": "Droogbak, Amsterdam", 
       "id": "050882"
     }, 
     {
       "lat": "4.89547070133899", 
       "lon": "52.3820539069972", 
       "name": "Droogbak, Amsterdam", 
       "id": "050892"
     }, 
     {
       "lat": "4.89304382780581", 
       "lon": "52.3836795646212", 
       "name": "Westerdoksdijk, Amsterdam", 
       "id": "050902"
     }, 
     {
       "lat": "4.89287745723862", 
       "lon": "52.3841102793355", 
       "name": "Westerdoksdijk, Amsterdam", 
       "id": "050912"
     }, 
     {
       "lat": "4.89159942558049", 
       "lon": "52.3893807083265", 
       "name": "Barentszplein, Amsterdam", 
       "id": "050922"
     }, 
     {
       "lat": "4.89155947715179", 
       "lon": "52.3890120462962", 
       "name": "Barentszplein, Amsterdam", 
       "id": "050932"
     }, 
     {
       "lat": "4.88487140468676", 
       "lon": "52.3880851001314", 
       "name": "Zoutkeetsgracht, Amsterdam", 
       "id": "050941"
     }, 
     {
       "lat": "4.90453176491359", 
       "lon": "52.3673154083127", 
       "name": "Mr. Visserplein, Amsterdam", 
       "id": "051052"
     }, 
     {
       "lat": "4.90099225890617", 
       "lon": "52.3767829549183", 
       "name": "Centraal Station, Amsterdam", 
       "id": "051132"
     }, 
     {
       "lat": "4.90198701339224", 
       "lon": "52.3771375553461", 
       "name": "Centraal Station, Amsterdam", 
       "id": "051142"
     }, 
     {
       "lat": "4.89130638439309", 
       "lon": "52.3735521529158", 
       "name": "Dam, Amsterdam", 
       "id": "051381"
     }, 
     {
       "lat": "4.89124220939995", 
       "lon": "52.372725014895", 
       "name": "Dam, Amsterdam", 
       "id": "051391"
     }, 
     {
       "lat": "4.89465700853933", 
       "lon": "52.3799384177117", 
       "name": "Singel, Amsterdam", 
       "id": "051412"
     }, 
     {
       "lat": "4.90091705951788", 
       "lon": "52.3769444246637", 
       "name": "Centraal Station, Amsterdam", 
       "id": "051512"
     }, 
     {
       "lat": "4.90282541463514", 
       "lon": "52.3676050342068", 
       "name": "Waterlooplein, Amsterdam", 
       "id": "051522"
     }, 
     {
       "lat": "4.89486602955628", 
       "lon": "52.37433995004", 
       "name": "Dam, Amsterdam", 
       "id": "051532"
     }, 
     {
       "lat": "4.85251969945997", 
       "lon": "52.3580682370796", 
       "name": "Surinameplein, Amsterdam", 
       "id": "060011"
     }, 
     {
       "lat": "4.85251969945997", 
       "lon": "52.3580682370796", 
       "name": "Surinameplein, Amsterdam", 
       "id": "060012"
     }, 
     {
       "lat": "4.85090491799144", 
       "lon": "52.3580699200789", 
       "name": "Surinameplein, Amsterdam", 
       "id": "060021"
     }, 
     {
       "lat": "4.85328805433332", 
       "lon": "52.3588716156913", 
       "name": "Hoofdweg, Amsterdam", 
       "id": "060061"
     }, 
     {
       "lat": "4.85328805433332", 
       "lon": "52.3588716156913", 
       "name": "Hoofdweg, Amsterdam", 
       "id": "060062"
     }, 
     {
       "lat": "4.85337007421198", 
       "lon": "52.3593753000352", 
       "name": "Hoofdweg, Amsterdam", 
       "id": "060071"
     }, 
     {
       "lat": "4.85337007421198", 
       "lon": "52.3593753000352", 
       "name": "Hoofdweg, Amsterdam", 
       "id": "060072"
     }, 
     {
       "lat": "4.85209314590156", 
       "lon": "52.3581382117112", 
       "name": "Surinameplein, Amsterdam", 
       "id": "060082"
     }, 
     {
       "lat": "4.85325863893486", 
       "lon": "52.3613161526824", 
       "name": "Corantijnstraat, Amsterdam", 
       "id": "060101"
     }, 
     {
       "lat": "4.85325863893486", 
       "lon": "52.3613161526824", 
       "name": "Corantijnstraat, Amsterdam", 
       "id": "060102"
     }, 
     {
       "lat": "4.85329683892074", 
       "lon": "52.3618016636599", 
       "name": "Corantijnstraat, Amsterdam", 
       "id": "060131"
     }, 
     {
       "lat": "4.85329683892074", 
       "lon": "52.3618016636599", 
       "name": "Corantijnstraat, Amsterdam", 
       "id": "060132"
     }, 
     {
       "lat": "4.85315862881752", 
       "lon": "52.3635266885472", 
       "name": "Postjesweg, Amsterdam", 
       "id": "060151"
     }, 
     {
       "lat": "4.85315862881752", 
       "lon": "52.3635266885472", 
       "name": "Postjesweg, Amsterdam", 
       "id": "060152"
     }, 
     {
       "lat": "4.86239373733525", 
       "lon": "52.3647274072564", 
       "name": "J.P. Heijestraat, Amsterdam", 
       "id": "060161"
     }, 
     {
       "lat": "4.86239373733525", 
       "lon": "52.3647274072564", 
       "name": "J.P. Heijestraat, Amsterdam", 
       "id": "060162"
     }, 
     {
       "lat": "4.86292055660021", 
       "lon": "52.3648735453101", 
       "name": "J.P. Heijestraat, Amsterdam", 
       "id": "060171"
     }, 
     {
       "lat": "4.86292055660021", 
       "lon": "52.3648735453101", 
       "name": "J.P. Heijestraat, Amsterdam", 
       "id": "060172"
     }, 
     {
       "lat": "4.86737161446223", 
       "lon": "52.3659177751412", 
       "name": "Ten Katestraat, Amsterdam", 
       "id": "060191"
     }, 
     {
       "lat": "4.86737161446223", 
       "lon": "52.3659177751412", 
       "name": "Ten Katestraat, Amsterdam", 
       "id": "060192"
     }, 
     {
       "lat": "4.86773728328558", 
       "lon": "52.3660362207285", 
       "name": "Ten Katestraat, Amsterdam", 
       "id": "060201"
     }, 
     {
       "lat": "4.86773728328558", 
       "lon": "52.3660362207285", 
       "name": "Ten Katestraat, Amsterdam", 
       "id": "060202"
     }, 
     {
       "lat": "4.87176227554324", 
       "lon": "52.3671233529577", 
       "name": "Bilderdijkstraat, Amsterdam", 
       "id": "060211"
     }, 
     {
       "lat": "4.87176227554324", 
       "lon": "52.3671233529577", 
       "name": "Bilderdijkstraat, Amsterdam", 
       "id": "060212"
     }, 
     {
       "lat": "4.87253770443101", 
       "lon": "52.3673604073481", 
       "name": "Bilderdijkstraat, Amsterdam", 
       "id": "060231"
     }, 
     {
       "lat": "4.87230623532827", 
       "lon": "52.3670628057808", 
       "name": "Kinkerstraat, Amsterdam", 
       "id": "060241"
     }, 
     {
       "lat": "4.87230623532827", 
       "lon": "52.3670628057808", 
       "name": "Kinkerstraat, Amsterdam", 
       "id": "060242"
     }, 
     {
       "lat": "4.87200831891464", 
       "lon": "52.3674300067477", 
       "name": "Kinkerstraat, Amsterdam", 
       "id": "060251"
     }, 
     {
       "lat": "4.87854927469179", 
       "lon": "52.3680874299378", 
       "name": "Elandsgracht, Amsterdam", 
       "id": "060271"
     }, 
     {
       "lat": "4.87854927469179", 
       "lon": "52.3680874299378", 
       "name": "Elandsgracht, Amsterdam", 
       "id": "060272"
     }, 
     {
       "lat": "4.87741432014922", 
       "lon": "52.3697452776367", 
       "name": "Elandsgracht, Amsterdam", 
       "id": "060281"
     }, 
     {
       "lat": "4.87741432014922", 
       "lon": "52.3697452776367", 
       "name": "Elandsgracht, Amsterdam", 
       "id": "060282"
     }, 
     {
       "lat": "4.87684107206087", 
       "lon": "52.3685204774188", 
       "name": "Elandsgracht, Amsterdam", 
       "id": "060291"
     }, 
     {
       "lat": "4.87587609732352", 
       "lon": "52.3719855751631", 
       "name": "Rozengracht, Amsterdam", 
       "id": "060301"
     }, 
     {
       "lat": "4.87587609732352", 
       "lon": "52.3719855751631", 
       "name": "Rozengracht, Amsterdam", 
       "id": "060302"
     }, 
     {
       "lat": "4.87082086058732", 
       "lon": "52.371055875874", 
       "name": "Bilderdijkstraat, Amsterdam", 
       "id": "060341"
     }, 
     {
       "lat": "4.86736458378631", 
       "lon": "52.3702767946594", 
       "name": "E. Wolffstraat, Amsterdam", 
       "id": "060361"
     }, 
     {
       "lat": "4.8698543912414", 
       "lon": "52.3708269637142", 
       "name": "Bilderdijkstraat, Amsterdam", 
       "id": "060371"
     }, 
     {
       "lat": "4.87040017907819", 
       "lon": "52.3706136418387", 
       "name": "De Clercqstraat, Amsterdam", 
       "id": "060381"
     }, 
     {
       "lat": "4.86699856484987", 
       "lon": "52.3701853097756", 
       "name": "E. Wolffstraat, Amsterdam", 
       "id": "060401"
     }, 
     {
       "lat": "4.87509884349505", 
       "lon": "52.3629944869395", 
       "name": "Overtoom , Amsterdam", 
       "id": "060431"
     }, 
     {
       "lat": "4.87509884349505", 
       "lon": "52.3629944869395", 
       "name": "Overtoom , Amsterdam", 
       "id": "060432"
     }, 
     {
       "lat": "4.87482930102693", 
       "lon": "52.3634516952549", 
       "name": "Overtoom , Amsterdam", 
       "id": "060441"
     }, 
     {
       "lat": "4.87482930102693", 
       "lon": "52.3634516952549", 
       "name": "Overtoom , Amsterdam", 
       "id": "060442"
     }, 
     {
       "lat": "4.87398967335607", 
       "lon": "52.3624234562698", 
       "name": "1e Con. Huygensstraat, Amsterdam", 
       "id": "060451"
     }, 
     {
       "lat": "4.87486821009365", 
       "lon": "52.3626249918154", 
       "name": "1e Con. Huygensstraat, Amsterdam", 
       "id": "060461"
     }, 
     {
       "lat": "4.86585107301244", 
       "lon": "52.3603746394906", 
       "name": "J.P. Heijestraat, Amsterdam", 
       "id": "060481"
     }, 
     {
       "lat": "4.86671516857592", 
       "lon": "52.3605492090398", 
       "name": "J.P. Heijestraat, Amsterdam", 
       "id": "060491"
     }, 
     {
       "lat": "4.85578163361342", 
       "lon": "52.3578132930719", 
       "name": "Overtoomsesluis, Amsterdam", 
       "id": "060521"
     }, 
     {
       "lat": "4.85661574446464", 
       "lon": "52.3580327409072", 
       "name": "Overtoomsesluis, Amsterdam", 
       "id": "060531"
     }, 
     {
       "lat": "4.87988407902968", 
       "lon": "52.3630690161491", 
       "name": "Stadhouderskade, Amsterdam", 
       "id": "060571"
     }, 
     {
       "lat": "4.88761829401063", 
       "lon": "52.3607111700232", 
       "name": "Spiegelgracht, Amsterdam", 
       "id": "060591"
     }, 
     {
       "lat": "4.8827246476703", 
       "lon": "52.3637372590913", 
       "name": "Leidseplein, Amsterdam", 
       "id": "060611"
     }, 
     {
       "lat": "4.88324378334373", 
       "lon": "52.3632721080764", 
       "name": "Leidseplein, Amsterdam", 
       "id": "060621"
     }, 
     {
       "lat": "4.88301172690202", 
       "lon": "52.3643136968066", 
       "name": "Leidseplein, Amsterdam", 
       "id": "060671"
     }, 
     {
       "lat": "4.88253216188728", 
       "lon": "52.3638802424092", 
       "name": "Leidseplein, Amsterdam", 
       "id": "060681"
     }, 
     {
       "lat": "4.88186083610004", 
       "lon": "52.3635268572089", 
       "name": "Leidseplein, Amsterdam", 
       "id": "060691"
     }, 
     {
       "lat": "4.88186083610004", 
       "lon": "52.3635268572089", 
       "name": "Leidseplein, Amsterdam", 
       "id": "060692"
     }, 
     {
       "lat": "4.884647241077", 
       "lon": "52.3650935954019", 
       "name": "Prinsengracht, Amsterdam", 
       "id": "060711"
     }, 
     {
       "lat": "4.88428173844031", 
       "lon": "52.3649572274007", 
       "name": "Prinsengracht, Amsterdam", 
       "id": "060721"
     }, 
     {
       "lat": "4.88666260510111", 
       "lon": "52.3660458444153", 
       "name": "Keizersgracht, Amsterdam", 
       "id": "060731"
     }, 
     {
       "lat": "4.88623866683709", 
       "lon": "52.365882272281", 
       "name": "Keizersgracht, Amsterdam", 
       "id": "060741"
     }, 
     {
       "lat": "4.88942531854651", 
       "lon": "52.3671360189943", 
       "name": "Koningsplein, Amsterdam", 
       "id": "060751"
     }, 
     {
       "lat": "4.88857649477811", 
       "lon": "52.3668897786873", 
       "name": "Koningsplein, Amsterdam", 
       "id": "060761"
     }, 
     {
       "lat": "4.87977295376623", 
       "lon": "52.3663670372636", 
       "name": "Raamplein, Amsterdam", 
       "id": "060771"
     }, 
     {
       "lat": "4.87977295376623", 
       "lon": "52.3663670372636", 
       "name": "Raamplein, Amsterdam", 
       "id": "060772"
     }, 
     {
       "lat": "4.87986587410527", 
       "lon": "52.3659450122386", 
       "name": "Raamplein, Amsterdam", 
       "id": "060781"
     }, 
     {
       "lat": "4.87986587410527", 
       "lon": "52.3659450122386", 
       "name": "Raamplein, Amsterdam", 
       "id": "060782"
     }, 
     {
       "lat": "4.86039093759693", 
       "lon": "52.3590562305329", 
       "name": "Rhijnvis Feithstraat, Amsterdam", 
       "id": "060811"
     }, 
     {
       "lat": "4.85967422166887", 
       "lon": "52.3588373326813", 
       "name": "Rhijnvis Feithstraat, Amsterdam", 
       "id": "060821"
     }, 
     {
       "lat": "4.88124691104989", 
       "lon": "52.3632905540034", 
       "name": "Leidseplein, Amsterdam", 
       "id": "060891"
     }, 
     {
       "lat": "4.88124691104989", 
       "lon": "52.3632905540034", 
       "name": "Leidseplein, Amsterdam", 
       "id": "060892"
     }, 
     {
       "lat": "4.85319747856063", 
       "lon": "52.3639582757747", 
       "name": "Postjesweg, Amsterdam", 
       "id": "061161"
     }, 
     {
       "lat": "4.85319747856063", 
       "lon": "52.3639582757747", 
       "name": "Postjesweg, Amsterdam", 
       "id": "061162"
     }, 
     {
       "lat": "4.87836675247361", 
       "lon": "52.3583978675634", 
       "name": "Van Baerlestraat, Amsterdam", 
       "id": "070021"
     }, 
     {
       "lat": "4.87808279882969", 
       "lon": "52.3588370460935", 
       "name": "Van Baerlestraat, Amsterdam", 
       "id": "070031"
     }, 
     {
       "lat": "4.87979854547514", 
       "lon": "52.3564267095707", 
       "name": "Museumplein, Amsterdam", 
       "id": "070061"
     }, 
     {
       "lat": "4.87979854547514", 
       "lon": "52.3564267095707", 
       "name": "Museumplein, Amsterdam", 
       "id": "070062"
     }, 
     {
       "lat": "4.87949952889104", 
       "lon": "52.3569017780083", 
       "name": "Museumplein, Amsterdam", 
       "id": "070071"
     }, 
     {
       "lat": "4.87949952889104", 
       "lon": "52.3569017780083", 
       "name": "Museumplein, Amsterdam", 
       "id": "070072"
     }, 
     {
       "lat": "4.87911483670757", 
       "lon": "52.3558845120866", 
       "name": "Museumplein, Amsterdam", 
       "id": "070101"
     }, 
     {
       "lat": "4.87959777731674", 
       "lon": "52.3560124124704", 
       "name": "Museumplein, Amsterdam", 
       "id": "070111"
     }, 
     {
       "lat": "4.88206709750882", 
       "lon": "52.3531468961827", 
       "name": "Roelof Hartplein, Amsterdam", 
       "id": "070151"
     }, 
     {
       "lat": "4.88206709750882", 
       "lon": "52.3531468961827", 
       "name": "Roelof Hartplein, Amsterdam", 
       "id": "070152"
     }, 
     {
       "lat": "4.88286426619507", 
       "lon": "52.3527458466404", 
       "name": "Roelof Hartplein, Amsterdam", 
       "id": "070161"
     }, 
     {
       "lat": "4.88205825087618", 
       "lon": "52.3526345566128", 
       "name": "Roelof Hartplein, Amsterdam", 
       "id": "070171"
     }, 
     {
       "lat": "4.88205825087618", 
       "lon": "52.3526345566128", 
       "name": "Roelof Hartplein, Amsterdam", 
       "id": "070172"
     }, 
     {
       "lat": "4.8853403770455", 
       "lon": "52.3544370797869", 
       "name": "Ruysdaelstraat, Amsterdam", 
       "id": "070191"
     }, 
     {
       "lat": "4.88608772242216", 
       "lon": "52.3545480989357", 
       "name": "Ruysdaelstraat, Amsterdam", 
       "id": "070201"
     }, 
     {
       "lat": "4.87444825438549", 
       "lon": "52.3570417850304", 
       "name": "Jac. Obrechtstraat, Amsterdam", 
       "id": "070251"
     }, 
     {
       "lat": "4.87482906652861", 
       "lon": "52.3571153359361", 
       "name": "Jac. Obrechtstraat, Amsterdam", 
       "id": "070261"
     }, 
     {
       "lat": "4.87051196963392", 
       "lon": "52.355973102107", 
       "name": "Corn. Schuytstraat, Amsterdam", 
       "id": "070271"
     }, 
     {
       "lat": "4.87087808782611", 
       "lon": "52.3560466016514", 
       "name": "Corn. Schuytstraat, Amsterdam", 
       "id": "070281"
     }, 
     {
       "lat": "4.8679092437591", 
       "lon": "52.3551078759511", 
       "name": "Emmastraat, Amsterdam", 
       "id": "070291"
     }, 
     {
       "lat": "4.86812741493617", 
       "lon": "52.3552796002265", 
       "name": "Emmastraat, Amsterdam", 
       "id": "070301"
     }, 
     {
       "lat": "4.86374682246086", 
       "lon": "52.3533279411506", 
       "name": "Valeriusplein, Amsterdam", 
       "id": "070311"
     }, 
     {
       "lat": "4.86326416917618", 
       "lon": "52.3531820015258", 
       "name": "Valeriusplein, Amsterdam", 
       "id": "070321"
     }, 
     {
       "lat": "4.8569566399558", 
       "lon": "52.3516170054351", 
       "name": "Amstelveenseweg, Amsterdam", 
       "id": "070331"
     }, 
     {
       "lat": "4.85596206537517", 
       "lon": "52.3513249370955", 
       "name": "Amstelveenseweg, Amsterdam", 
       "id": "070341"
     }, 
     {
       "lat": "4.85596206537517", 
       "lon": "52.3513249370955", 
       "name": "Amstelveenseweg, Amsterdam", 
       "id": "070342"
     }, 
     {
       "lat": "4.85672632399741", 
       "lon": "52.3512384871166", 
       "name": "Zeilstraat, Amsterdam", 
       "id": "070351"
     }, 
     {
       "lat": "4.85672632399741", 
       "lon": "52.3512384871166", 
       "name": "Zeilstraat, Amsterdam", 
       "id": "070352"
     }, 
     {
       "lat": "4.85043845084002", 
       "lon": "52.3553714766233", 
       "name": "Haarlemmermeerstraat, Amsterdam", 
       "id": "070442"
     }, 
     {
       "lat": "4.85023600439902", 
       "lon": "52.3551189009573", 
       "name": "Haarlemmermeerstraat, Amsterdam", 
       "id": "070452"
     }, 
     {
       "lat": "4.8504791026497", 
       "lon": "52.3520102351935", 
       "name": "Hoofddorpplein, Amsterdam", 
       "id": "070462"
     }, 
     {
       "lat": "4.85010316044192", 
       "lon": "52.3515411656685", 
       "name": "Hoofddorpplein, Amsterdam", 
       "id": "070481"
     }, 
     {
       "lat": "4.85010316044192", 
       "lon": "52.3515411656685", 
       "name": "Hoofddorpplein, Amsterdam", 
       "id": "070482"
     }, 
     {
       "lat": "4.8496086165112", 
       "lon": "52.3511704217745", 
       "name": "Hoofddorpplein, Amsterdam", 
       "id": "070491"
     }, 
     {
       "lat": "4.8496086165112", 
       "lon": "52.3511704217745", 
       "name": "Hoofddorpplein, Amsterdam", 
       "id": "070492"
     }, 
     {
       "lat": "4.85729468121999", 
       "lon": "52.3491199189744", 
       "name": "Haarl'meerstation, Amsterdam", 
       "id": "070572"
     }, 
     {
       "lat": "4.85711975111354", 
       "lon": "52.3490202701488", 
       "name": "Haarl'meerstation, Amsterdam", 
       "id": "070582"
     }, 
     {
       "lat": "4.85725161927109", 
       "lon": "52.3490388362115", 
       "name": "Haarl'meerstation, Amsterdam", 
       "id": "070592"
     }, 
     {
       "lat": "4.8575022888374", 
       "lon": "52.3489410928167", 
       "name": "Haarl'meerstation, Amsterdam", 
       "id": "070611"
     }, 
     {
       "lat": "4.8575429917589", 
       "lon": "52.3492198959402", 
       "name": "Haarl'meerstation, Amsterdam", 
       "id": "070621"
     }, 
     {
       "lat": "4.86416344562253", 
       "lon": "52.3516041323737", 
       "name": "Valeriusplein, Amsterdam", 
       "id": "070651"
     }, 
     {
       "lat": "4.86507033689414", 
       "lon": "52.3518687815246", 
       "name": "Valeriusplein, Amsterdam", 
       "id": "070661"
     }, 
     {
       "lat": "4.86966628493671", 
       "lon": "52.3529674972267", 
       "name": "Emmastraat, Amsterdam", 
       "id": "070691"
     }, 
     {
       "lat": "4.87013354684497", 
       "lon": "52.3531762577586", 
       "name": "Emmastraat, Amsterdam", 
       "id": "070701"
     }, 
     {
       "lat": "4.87603089006101", 
       "lon": "52.3547297904675", 
       "name": "Jac. Obrechtstraat, Amsterdam", 
       "id": "070731"
     }, 
     {
       "lat": "4.87649892450039", 
       "lon": "52.3548756147227", 
       "name": "Jac. Obrechtstraat, Amsterdam", 
       "id": "070741"
     }, 
     {
       "lat": "4.87886424459724", 
       "lon": "52.3508502949541", 
       "name": "Apollolaan, Amsterdam", 
       "id": "070791"
     }, 
     {
       "lat": "4.87886424459724", 
       "lon": "52.3508502949541", 
       "name": "Apollolaan, Amsterdam", 
       "id": "070792"
     }, 
     {
       "lat": "4.87912348353353", 
       "lon": "52.3512828203291", 
       "name": "Apollolaan, Amsterdam", 
       "id": "070801"
     }, 
     {
       "lat": "4.87912348353353", 
       "lon": "52.3512828203291", 
       "name": "Apollolaan, Amsterdam", 
       "id": "070802"
     }, 
     {
       "lat": "4.87735667705388", 
       "lon": "52.3492080385913", 
       "name": "Gerrit v.d. Veenstr, Amsterdam", 
       "id": "070831"
     }, 
     {
       "lat": "4.87735667705388", 
       "lon": "52.3492080385913", 
       "name": "Gerrit v.d. Veenstr, Amsterdam", 
       "id": "070832"
     }, 
     {
       "lat": "4.87719916550974", 
       "lon": "52.3488658250738", 
       "name": "Gerrit v.d. Veenstr, Amsterdam", 
       "id": "070841"
     }, 
     {
       "lat": "4.87719916550974", 
       "lon": "52.3488658250738", 
       "name": "Gerrit v.d. Veenstr, Amsterdam", 
       "id": "070842"
     }, 
     {
       "lat": "4.87688135648024", 
       "lon": "52.3471477924844", 
       "name": "Stadionweg, Amsterdam", 
       "id": "070871"
     }, 
     {
       "lat": "4.87688135648024", 
       "lon": "52.3471477924844", 
       "name": "Stadionweg, Amsterdam", 
       "id": "070872"
     }, 
     {
       "lat": "4.87687236403354", 
       "lon": "52.3466534266341", 
       "name": "Stadionweg, Amsterdam", 
       "id": "070881"
     }, 
     {
       "lat": "4.87687236403354", 
       "lon": "52.3466534266341", 
       "name": "Stadionweg, Amsterdam", 
       "id": "070882"
     }, 
     {
       "lat": "4.87299657315245", 
       "lon": "52.3467714678317", 
       "name": "Minervaplein, Amsterdam", 
       "id": "070911"
     }, 
     {
       "lat": "4.87204352297724", 
       "lon": "52.346695421223", 
       "name": "Minervaplein, Amsterdam", 
       "id": "070941"
     }, 
     {
       "lat": "4.86582560355273", 
       "lon": "52.3462996946452", 
       "name": "Olympiaplein, Amsterdam", 
       "id": "070971"
     }, 
     {
       "lat": "4.86582560355273", 
       "lon": "52.3462996946452", 
       "name": "Olympiaplein, Amsterdam", 
       "id": "070972"
     }, 
     {
       "lat": "4.86658796472203", 
       "lon": "52.3463659649835", 
       "name": "Olympiaplein, Amsterdam", 
       "id": "070981"
     }, 
     {
       "lat": "4.86658796472203", 
       "lon": "52.3463659649835", 
       "name": "Olympiaplein, Amsterdam", 
       "id": "070982"
     }, 
     {
       "lat": "4.85873468865674", 
       "lon": "52.3452795893097", 
       "name": "Olympiaweg, Amsterdam", 
       "id": "071081"
     }, 
     {
       "lat": "4.85873468865674", 
       "lon": "52.3452795893097", 
       "name": "Olympiaweg, Amsterdam", 
       "id": "071082"
     }, 
     {
       "lat": "4.8568469199264", 
       "lon": "52.3374607576705", 
       "name": "Amstelveenseweg, Amsterdam", 
       "id": "071122"
     }, 
     {
       "lat": "4.85760148100956", 
       "lon": "52.3492381332134", 
       "name": "Haarl'meerstation, Amsterdam", 
       "id": "071162"
     }, 
     {
       "lat": "4.8583386878447", 
       "lon": "52.3452598448446", 
       "name": "Olympiaweg, Amsterdam", 
       "id": "071201"
     }, 
     {
       "lat": "4.8583386878447", 
       "lon": "52.3452598448446", 
       "name": "Olympiaweg, Amsterdam", 
       "id": "071202"
     }, 
     {
       "lat": "4.85696188243783", 
       "lon": "52.3438066515926", 
       "name": "Stadionplein, Amsterdam", 
       "id": "071211"
     }, 
     {
       "lat": "4.85696188243783", 
       "lon": "52.3438066515926", 
       "name": "Stadionplein, Amsterdam", 
       "id": "071212"
     }, 
     {
       "lat": "4.87664389580073", 
       "lon": "52.3320652766482", 
       "name": "Gelderlandplein, Amsterdam", 
       "id": "071222"
     }, 
     {
       "lat": "4.87636412639837", 
       "lon": "52.3321539470881", 
       "name": "Gelderlandplein, Amsterdam", 
       "id": "071232"
     }, 
     {
       "lat": "4.86976363774624", 
       "lon": "52.3320264019018", 
       "name": "A.J. Ernststraat, Amsterdam", 
       "id": "071242"
     }, 
     {
       "lat": "4.8697625905667", 
       "lon": "52.3321162752798", 
       "name": "A.J. Ernststraat, Amsterdam", 
       "id": "071252"
     }, 
     {
       "lat": "4.86833455466446", 
       "lon": "52.3400732034171", 
       "name": "Strawinskylaan, Amsterdam", 
       "id": "071282"
     }, 
     {
       "lat": "4.86854078981647", 
       "lon": "52.3412604945969", 
       "name": "Strawinskylaan, Amsterdam", 
       "id": "071292"
     }, 
     {
       "lat": "4.86819437305766", 
       "lon": "52.3420229371456", 
       "name": "Pr. Irenestraat, Amsterdam", 
       "id": "071302"
     }, 
     {
       "lat": "4.86832934437033", 
       "lon": "52.3430301601345", 
       "name": "Pr. Irenestraat, Amsterdam", 
       "id": "071312"
     }, 
     {
       "lat": "4.86783501591812", 
       "lon": "52.3351097536351", 
       "name": "De Boelelaan, Amsterdam", 
       "id": "071322"
     }, 
     {
       "lat": "4.86754327307302", 
       "lon": "52.3349646681331", 
       "name": "De Boelelaan, Amsterdam", 
       "id": "071332"
     }, 
     {
       "lat": "4.86186434229381", 
       "lon": "52.3325578262776", 
       "name": "Overijsselweg, Amsterdam", 
       "id": "071342"
     }, 
     {
       "lat": "4.8617570811475", 
       "lon": "52.3317035089632", 
       "name": "Overijsselweg, Amsterdam", 
       "id": "071352"
     }, 
     {
       "lat": "4.86188071634917", 
       "lon": "52.3286931435999", 
       "name": "Egelenburg, Amsterdam", 
       "id": "071372"
     }, 
     {
       "lat": "4.86176836043881", 
       "lon": "52.328270217774", 
       "name": "Egelenburg, Amsterdam", 
       "id": "071382"
     }, 
     {
       "lat": "4.86860527005821", 
       "lon": "52.3344839863932", 
       "name": "De Boelelaan/VU, Amsterdam", 
       "id": "071392"
     }, 
     {
       "lat": "4.86907180837015", 
       "lon": "52.3347376882798", 
       "name": "De Boelelaan/VU, Amsterdam", 
       "id": "071402"
     }, 
     {
       "lat": "4.88183656939149", 
       "lon": "52.3321414946723", 
       "name": "Oldengaarde, Amsterdam", 
       "id": "071442"
     }, 
     {
       "lat": "4.88296720533264", 
       "lon": "52.3320564402046", 
       "name": "Oldengaarde, Amsterdam", 
       "id": "071462"
     }, 
     {
       "lat": "4.88823314036888", 
       "lon": "52.3321416773555", 
       "name": "Weerdestein, Amsterdam", 
       "id": "071482"
     }, 
     {
       "lat": "4.8886594883111", 
       "lon": "52.3320625843552", 
       "name": "Weerdestein, Amsterdam", 
       "id": "071492"
     }, 
     {
       "lat": "4.8897382176777", 
       "lon": "52.3339905096729", 
       "name": "Europaboulevard, Amsterdam", 
       "id": "071502"
     }, 
     {
       "lat": "4.89010618132842", 
       "lon": "52.3351964183793", 
       "name": "Europaboulevard, Amsterdam", 
       "id": "071512"
     }, 
     {
       "lat": "4.88199232649906", 
       "lon": "52.3248979974214", 
       "name": "Van Heenvlietlaan, Amsterdam", 
       "id": "071572"
     }, 
     {
       "lat": "4.88334228658474", 
       "lon": "52.324858815124", 
       "name": "Van Heenvlietlaan, Amsterdam", 
       "id": "071582"
     }, 
     {
       "lat": "4.8888272874814", 
       "lon": "52.3249539489866", 
       "name": "Bleyenbeek, Amsterdam", 
       "id": "071592"
     }, 
     {
       "lat": "4.88845957919229", 
       "lon": "52.3250422774987", 
       "name": "Bleyenbeek, Amsterdam", 
       "id": "071602"
     }, 
     {
       "lat": "4.87700605673221", 
       "lon": "52.3248046982165", 
       "name": "Backershagen, Amsterdam", 
       "id": "071612"
     }, 
     {
       "lat": "4.87515904181145", 
       "lon": "52.3246978531943", 
       "name": "Backershagen, Amsterdam", 
       "id": "071622"
     }, 
     {
       "lat": "4.86998244224016", 
       "lon": "52.3245764704733", 
       "name": "Van Boshuizenstraat, Amsterdam", 
       "id": "071632"
     }, 
     {
       "lat": "4.86881520607645", 
       "lon": "52.3240410812059", 
       "name": "Van Boshuizenstraat, Amsterdam", 
       "id": "071652"
     }, 
     {
       "lat": "4.86500637874762", 
       "lon": "52.323619879782", 
       "name": "Noordhollandstraat, Amsterdam", 
       "id": "071662"
     }, 
     {
       "lat": "4.86541770170599", 
       "lon": "52.3235677676699", 
       "name": "Noordhollandstraat, Amsterdam", 
       "id": "071672"
     }, 
     {
       "lat": "4.86136873821047", 
       "lon": "52.3236127559607", 
       "name": "Bolestein, Amsterdam", 
       "id": "071682"
     }, 
     {
       "lat": "4.86260165526787", 
       "lon": "52.323546326742", 
       "name": "Bolestein, Amsterdam", 
       "id": "071692"
     }, 
     {
       "lat": "4.86905970454013", 
       "lon": "52.3282304701115", 
       "name": "Van Nijenrodeweg, Amsterdam", 
       "id": "071702"
     }, 
     {
       "lat": "4.86865915033257", 
       "lon": "52.3273568983546", 
       "name": "Van Nijenrodeweg, Amsterdam", 
       "id": "071712"
     }, 
     {
       "lat": "4.86907236234422", 
       "lon": "52.3309178779079", 
       "name": "G. van IJselsteinstraat, Amsterdam", 
       "id": "071802"
     }, 
     {
       "lat": "4.8686265983209", 
       "lon": "52.3314012662162", 
       "name": "A.J. Ernststraat, Amsterdam", 
       "id": "071812"
     }, 
     {
       "lat": "4.87677222001155", 
       "lon": "52.3425995108984", 
       "name": "Pr. Irenestraat, Amsterdam", 
       "id": "071861"
     }, 
     {
       "lat": "4.87677222001155", 
       "lon": "52.3425995108984", 
       "name": "Pr. Irenestraat, Amsterdam", 
       "id": "071862"
     }, 
     {
       "lat": "4.87678079735454", 
       "lon": "52.3431298264567", 
       "name": "Pr. Irenestraat, Amsterdam", 
       "id": "071871"
     }, 
     {
       "lat": "4.87678079735454", 
       "lon": "52.3431298264567", 
       "name": "Pr. Irenestraat, Amsterdam", 
       "id": "071872"
     }, 
     {
       "lat": "4.87341847058785", 
       "lon": "52.3407514923172", 
       "name": "Station Zuid, Amsterdam", 
       "id": "071912"
     }, 
     {
       "lat": "4.87287452257857", 
       "lon": "52.3408390073255", 
       "name": "Station Zuid, Amsterdam", 
       "id": "071922"
     }, 
     {
       "lat": "4.87063055536129", 
       "lon": "52.3029006625886", 
       "name": "Oranjebaan, Amstelveen", 
       "id": "071972"
     }, 
     {
       "lat": "4.87333612706924", 
       "lon": "52.3034876706393", 
       "name": "Oranjebaan, Amstelveen", 
       "id": "071982"
     }, 
     {
       "lat": "4.85684159032382", 
       "lon": "52.3440487827175", 
       "name": "Stadionplein, Amsterdam", 
       "id": "072021"
     }, 
     {
       "lat": "4.85684159032382", 
       "lon": "52.3440487827175", 
       "name": "Stadionplein, Amsterdam", 
       "id": "072022"
     }, 
     {
       "lat": "4.85773556012171", 
       "lon": "52.3416889982993", 
       "name": "IJsbaanpad, Amsterdam", 
       "id": "072051"
     }, 
     {
       "lat": "4.85773556012171", 
       "lon": "52.3416889982993", 
       "name": "IJsbaanpad, Amsterdam", 
       "id": "072052"
     }, 
     {
       "lat": "4.85755885101009", 
       "lon": "52.3405108074317", 
       "name": "IJsbaanpad, Amsterdam", 
       "id": "072071"
     }, 
     {
       "lat": "4.85755885101009", 
       "lon": "52.3405108074317", 
       "name": "IJsbaanpad, Amsterdam", 
       "id": "072072"
     }, 
     {
       "lat": "4.85754680951206", 
       "lon": "52.3267594186118", 
       "name": "Van Nijenrodeweg, Amsterdam", 
       "id": "072202"
     }, 
     {
       "lat": "4.85741243453201", 
       "lon": "52.3269565488687", 
       "name": "Van Nijenrodeweg, Amsterdam", 
       "id": "072222"
     }, 
     {
       "lat": "4.88119667860525", 
       "lon": "52.3561091354959", 
       "name": "Museumplein, Amsterdam", 
       "id": "072301"
     }, 
     {
       "lat": "4.88037305423836", 
       "lon": "52.3562494158591", 
       "name": "Museumplein, Amsterdam", 
       "id": "072311"
     }, 
     {
       "lat": "4.86937980535632", 
       "lon": "52.3221651010154", 
       "name": "Uilenstede, Amsterdam", 
       "id": "072422"
     }, 
     {
       "lat": "4.86891476027609", 
       "lon": "52.3217945642768", 
       "name": "Uilenstede, Amsterdam", 
       "id": "072442"
     }, 
     {
       "lat": "4.86925429179634", 
       "lon": "52.3241238945495", 
       "name": "Van Boshuizenstraat, Amsterdam", 
       "id": "072522"
     }, 
     {
       "lat": "4.8893623361866", 
       "lon": "52.3361100446266", 
       "name": "Drentepark, Amsterdam", 
       "id": "072581"
     }, 
     {
       "lat": "4.89077463540269", 
       "lon": "52.3370866574238", 
       "name": "Station RAI, Amsterdam", 
       "id": "072601"
     }, 
     {
       "lat": "4.89077463540269", 
       "lon": "52.3370866574238", 
       "name": "Station RAI, Amsterdam", 
       "id": "072602"
     }, 
     {
       "lat": "4.89068801047909", 
       "lon": "52.3369604651617", 
       "name": "Station RAI, Amsterdam", 
       "id": "072611"
     }, 
     {
       "lat": "4.89068801047909", 
       "lon": "52.3369604651617", 
       "name": "Station RAI, Amsterdam", 
       "id": "072612"
     }, 
     {
       "lat": "4.87428346026946", 
       "lon": "52.3408181589093", 
       "name": "Station Zuid, Amsterdam", 
       "id": "072681"
     }, 
     {
       "lat": "4.87374044859149", 
       "lon": "52.340824791954", 
       "name": "Station Zuid, Amsterdam", 
       "id": "072691"
     }, 
     {
       "lat": "4.86873955933414", 
       "lon": "52.3380617148452", 
       "name": "Parnassusweg, Amsterdam", 
       "id": "072701"
     }, 
     {
       "lat": "4.86866483356385", 
       "lon": "52.3381782286479", 
       "name": "Parnassusweg, Amsterdam", 
       "id": "072711"
     }, 
     {
       "lat": "4.87291822982263", 
       "lon": "52.3408661606058", 
       "name": "Station Zuid, Amsterdam", 
       "id": "072922"
     }, 
     {
       "lat": "4.87327205109882", 
       "lon": "52.3407238932186", 
       "name": "Station Zuid, Amsterdam", 
       "id": "072942"
     }, 
     {
       "lat": "4.87959079666146", 
       "lon": "52.3309544813504", 
       "name": "Loowaard, Amsterdam", 
       "id": "072992"
     }, 
     {
       "lat": "4.87937300859517", 
       "lon": "52.3307558154267", 
       "name": "Loowaard, Amsterdam", 
       "id": "073002"
     }, 
     {
       "lat": "4.86096800830419", 
       "lon": "52.3351513170701", 
       "name": "VU medisch centrum, Amsterdam", 
       "id": "073031"
     }, 
     {
       "lat": "4.86096800830419", 
       "lon": "52.3351513170701", 
       "name": "VU medisch centrum, Amsterdam", 
       "id": "073032"
     }, 
     {
       "lat": "4.86013003831106", 
       "lon": "52.3352913923098", 
       "name": "VU medisch centrum, Amsterdam", 
       "id": "073042"
     }, 
     {
       "lat": "4.87820388386999", 
       "lon": "52.3470006955018", 
       "name": "Beethovenstraat, Amsterdam", 
       "id": "073072"
     }, 
     {
       "lat": "4.8763269023263", 
       "lon": "52.3468667798019", 
       "name": "Beethovenstraat, Amsterdam", 
       "id": "073081"
     }, 
     {
       "lat": "4.88187427338239", 
       "lon": "52.3481668567233", 
       "name": "Apollolaan, Amsterdam", 
       "id": "073092"
     }, 
     {
       "lat": "4.88210918568653", 
       "lon": "52.3481588716818", 
       "name": "Apollolaan, Amsterdam", 
       "id": "073102"
     }, 
     {
       "lat": "4.88653726304298", 
       "lon": "52.3602392408393", 
       "name": "Ruysdaelkade, Amsterdam", 
       "id": "073112"
     }, 
     {
       "lat": "4.88668334970365", 
       "lon": "52.3603027727311", 
       "name": "Ruysdaelkade, Amsterdam", 
       "id": "073122"
     }, 
     {
       "lat": "4.8789553538214", 
       "lon": "52.3582745677463", 
       "name": "Van Baerlestraat, Amsterdam", 
       "id": "073211"
     }, 
     {
       "lat": "4.87971681000475", 
       "lon": "52.3584396139392", 
       "name": "Van Baerlestraat, Amsterdam", 
       "id": "073221"
     }, 
     {
       "lat": "4.88354782223541", 
       "lon": "52.3597681853905", 
       "name": "Hobbemastraat, Amsterdam", 
       "id": "073231"
     }, 
     {
       "lat": "4.88354782223541", 
       "lon": "52.3597681853905", 
       "name": "Hobbemastraat, Amsterdam", 
       "id": "073232"
     }, 
     {
       "lat": "4.88332303770654", 
       "lon": "52.360171677018", 
       "name": "Hobbemastraat, Amsterdam", 
       "id": "073241"
     }, 
     {
       "lat": "4.88332303770654", 
       "lon": "52.360171677018", 
       "name": "Hobbemastraat, Amsterdam", 
       "id": "073242"
     }, 
     {
       "lat": "4.88311682353411", 
       "lon": "52.3279226937135", 
       "name": "Bouvigne, Amsterdam", 
       "id": "073312"
     }, 
     {
       "lat": "4.88293916367331", 
       "lon": "52.3280657414056", 
       "name": "Bouvigne, Amsterdam", 
       "id": "073322"
     }, 
     {
       "lat": "4.88985683897988", 
       "lon": "52.326018841072", 
       "name": "Nieuw Herlaer, Amsterdam", 
       "id": "073392"
     }, 
     {
       "lat": "4.89031276343274", 
       "lon": "52.325912903138", 
       "name": "Nieuw Herlaer, Amsterdam", 
       "id": "073402"
     }, 
     {
       "lat": "4.86869289747543", 
       "lon": "52.3395444948405", 
       "name": "Strawinskylaan, Amsterdam", 
       "id": "073412"
     }, 
     {
       "lat": "4.857201813075", 
       "lon": "52.3384599927295", 
       "name": "Amstelveenseweg, Amsterdam", 
       "id": "073423"
     }, 
     {
       "lat": "4.85798062716898", 
       "lon": "52.3383646125263", 
       "name": "Amstelveenseweg, Amsterdam", 
       "id": "073433"
     }, 
     {
       "lat": "4.86162384618354", 
       "lon": "52.3367630469386", 
       "name": "Gustav Mahlerlaan, Amsterdam", 
       "id": "073491"
     }, 
     {
       "lat": "4.86005785528387", 
       "lon": "52.3351922050144", 
       "name": "VU medisch centrum, Amsterdam", 
       "id": "073501"
     }, 
     {
       "lat": "4.86005785528387", 
       "lon": "52.3351922050144", 
       "name": "VU medisch centrum, Amsterdam", 
       "id": "073502"
     }, 
     {
       "lat": "4.91727315811919", 
       "lon": "52.331568510421", 
       "name": "Overamstel, Amsterdam", 
       "id": "074003"
     }, 
     {
       "lat": "4.91721362131114", 
       "lon": "52.3316491638821", 
       "name": "Overamstel, Amsterdam", 
       "id": "074013"
     }, 
     {
       "lat": "4.88981743325704", 
       "lon": "52.3373972102045", 
       "name": "Station RAI, Amsterdam", 
       "id": "074043"
     }, 
     {
       "lat": "4.88921043494989", 
       "lon": "52.3378799971977", 
       "name": "Station RAI, Amsterdam", 
       "id": "074053"
     }, 
     {
       "lat": "4.87471339791338", 
       "lon": "52.3391662702643", 
       "name": "Station Zuid, Amsterdam", 
       "id": "074083"
     }, 
     {
       "lat": "4.87375790973689", 
       "lon": "52.3393149208225", 
       "name": "Station Zuid, Amsterdam", 
       "id": "074093"
     }, 
     {
       "lat": "4.86886567773216", 
       "lon": "52.3347997000741", 
       "name": "De Boelelaan/VU, Amsterdam", 
       "id": "074101"
     }, 
     {
       "lat": "4.86880993073629", 
       "lon": "52.3345477977013", 
       "name": "De Boelelaan/VU, Amsterdam", 
       "id": "074111"
     }, 
     {
       "lat": "4.86885562258461", 
       "lon": "52.3344041931886", 
       "name": "De Boelelaan/VU, Amsterdam", 
       "id": "074123"
     }, 
     {
       "lat": "4.8688022892666", 
       "lon": "52.3339455821288", 
       "name": "De Boelelaan/VU, Amsterdam", 
       "id": "074133"
     }, 
     {
       "lat": "4.86887105920686", 
       "lon": "52.3318247638038", 
       "name": "A.J. Ernststraat, Amsterdam", 
       "id": "074141"
     }, 
     {
       "lat": "4.86881468640617", 
       "lon": "52.3316267853161", 
       "name": "A.J. Ernststraat, Amsterdam", 
       "id": "074151"
     }, 
     {
       "lat": "4.86887494039126", 
       "lon": "52.3314922323162", 
       "name": "A.J. Ernststraat, Amsterdam", 
       "id": "074163"
     }, 
     {
       "lat": "4.86882150536083", 
       "lon": "52.3310426083452", 
       "name": "A.J. Ernststraat, Amsterdam", 
       "id": "074173"
     }, 
     {
       "lat": "4.86902295382536", 
       "lon": "52.3250935649752", 
       "name": "Van Boshuizenstraat, Amsterdam", 
       "id": "074181"
     }, 
     {
       "lat": "4.86896679850164", 
       "lon": "52.3248776116097", 
       "name": "Van Boshuizenstraat, Amsterdam", 
       "id": "074191"
     }, 
     {
       "lat": "4.86898732664647", 
       "lon": "52.3256326774143", 
       "name": "Van Boshuizenstraat, Amsterdam", 
       "id": "074203"
     }, 
     {
       "lat": "4.86894846046552", 
       "lon": "52.3251921045857", 
       "name": "Van Boshuizenstraat, Amsterdam", 
       "id": "074213"
     }, 
     {
       "lat": "4.86924214743004", 
       "lon": "52.3213915464056", 
       "name": "Uilenstede, Amstelveen", 
       "id": "074221"
     }, 
     {
       "lat": "4.86911287187534", 
       "lon": "52.3211572971601", 
       "name": "Uilenstede, Amstelveen", 
       "id": "074231"
     }, 
     {
       "lat": "4.86920568764217", 
       "lon": "52.322002558148", 
       "name": "Uilenstede, Amstelveen", 
       "id": "074243"
     }, 
     {
       "lat": "4.86909411721897", 
       "lon": "52.3215077398134", 
       "name": "Uilenstede, Amstelveen", 
       "id": "074253"
     }, 
     {
       "lat": "4.87040028645633", 
       "lon": "52.3163993841262", 
       "name": "Kronenburg, Amstelveen", 
       "id": "074261"
     }, 
     {
       "lat": "4.87044689506752", 
       "lon": "52.3161748921595", 
       "name": "Kronenburg, Amstelveen", 
       "id": "074271"
     }, 
     {
       "lat": "4.87012982957147", 
       "lon": "52.3169554472779", 
       "name": "Kronenburg, Amstelveen", 
       "id": "074283"
     }, 
     {
       "lat": "4.87029658508014", 
       "lon": "52.3164888092727", 
       "name": "Kronenburg, Amstelveen", 
       "id": "074293"
     }, 
     {
       "lat": "4.87225055280812", 
       "lon": "52.3123988828168", 
       "name": "Zonnestein, Amstelveen", 
       "id": "074301"
     }, 
     {
       "lat": "4.87226865356898", 
       "lon": "52.3121023632598", 
       "name": "Zonnestein, Amstelveen", 
       "id": "074311"
     }, 
     {
       "lat": "4.8720540886491", 
       "lon": "52.3129013457742", 
       "name": "Zonnestein, Amstelveen", 
       "id": "074323"
     }, 
     {
       "lat": "4.87217629632904", 
       "lon": "52.3124794499909", 
       "name": "Zonnestein, Amstelveen", 
       "id": "074333"
     }, 
     {
       "lat": "4.87261520426522", 
       "lon": "52.3087693857337", 
       "name": "Onderuit, Amstelveen", 
       "id": "074341"
     }, 
     {
       "lat": "4.87259264388064", 
       "lon": "52.3081850782927", 
       "name": "Onderuit, Amstelveen", 
       "id": "074363"
     }, 
     {
       "lat": "4.87243427239422", 
       "lon": "52.3079327297513", 
       "name": "Onderuit, Amstelveen", 
       "id": "074371"
     }, 
     {
       "lat": "4.87243427239422", 
       "lon": "52.3079327297513", 
       "name": "Onderuit, Amstelveen", 
       "id": "074373"
     }, 
     {
       "lat": "4.87191965111853", 
       "lon": "52.3029961643358", 
       "name": "Oranjebaan, Amstelveen", 
       "id": "074381"
     }, 
     {
       "lat": "4.87162925216744", 
       "lon": "52.3027522269563", 
       "name": "Oranjebaan, Amstelveen", 
       "id": "074391"
     }, 
     {
       "lat": "4.8721917476423", 
       "lon": "52.3035545958354", 
       "name": "Oranjebaan, Amstelveen", 
       "id": "074403"
     }, 
     {
       "lat": "4.87183012383424", 
       "lon": "52.3031305919307", 
       "name": "Oranjebaan, Amstelveen", 
       "id": "074413"
     }, 
     {
       "lat": "4.86751240687597", 
       "lon": "52.3012422260257", 
       "name": "Binnenhof, Amstelveen", 
       "id": "074451"
     }, 
     {
       "lat": "4.87006136161593", 
       "lon": "52.3001568812895", 
       "name": "Amstelveen Centrum, Amstelveen", 
       "id": "074503"
     }, 
     {
       "lat": "4.86964104262601", 
       "lon": "52.2997416014484", 
       "name": "Amstelveen Centrum, Amstelveen", 
       "id": "074513"
     }, 
     {
       "lat": "4.86778765460932", 
       "lon": "52.2965068357097", 
       "name": "Ouderkerkerlaan, Amstelveen", 
       "id": "074543"
     }, 
     {
       "lat": "4.86733870508127", 
       "lon": "52.2960374943094", 
       "name": "Ouderkerkerlaan, Amstelveen", 
       "id": "074553"
     }, 
     {
       "lat": "4.86426112016805", 
       "lon": "52.2909817323181", 
       "name": "Sportlaan, Amstelveen", 
       "id": "074583"
     }, 
     {
       "lat": "4.86387110130621", 
       "lon": "52.2904946618251", 
       "name": "Sportlaan, Amstelveen", 
       "id": "074593"
     }, 
     {
       "lat": "4.86159403896152", 
       "lon": "52.2872129754976", 
       "name": "Marne, Amstelveen", 
       "id": "074623"
     }, 
     {
       "lat": "4.86114524842605", 
       "lon": "52.2867436099606", 
       "name": "Marne, Amstelveen", 
       "id": "074633"
     }, 
     {
       "lat": "4.85951298214573", 
       "lon": "52.2847320389113", 
       "name": "Gondel, Amstelveen", 
       "id": "074663"
     }, 
     {
       "lat": "4.85915173860518", 
       "lon": "52.2842990076697", 
       "name": "Gondel, Amstelveen", 
       "id": "074673"
     }, 
     {
       "lat": "4.85745837267938", 
       "lon": "52.2812804901249", 
       "name": "Meent, Amstelveen", 
       "id": "074703"
     }, 
     {
       "lat": "4.85693566872522", 
       "lon": "52.2808736917991", 
       "name": "Meent, Amstelveen", 
       "id": "074713"
     }, 
     {
       "lat": "4.85214845437988", 
       "lon": "52.2804836201872", 
       "name": "Brink, Amstelveen", 
       "id": "074743"
     }, 
     {
       "lat": "4.8513994075662", 
       "lon": "52.280624034277", 
       "name": "Brink, Amstelveen", 
       "id": "074753"
     }, 
     {
       "lat": "4.84509450980462", 
       "lon": "52.2833276138336", 
       "name": "Poortwachter, Amstelveen", 
       "id": "074783"
     }, 
     {
       "lat": "4.84584427838202", 
       "lon": "52.2831333154952", 
       "name": "Poortwachter, Amstelveen", 
       "id": "074793"
     }, 
     {
       "lat": "4.8603385991668", 
       "lon": "52.2756579504955", 
       "name": "Galjoen, Amstelveen", 
       "id": "074802"
     }, 
     {
       "lat": "4.8573089172958", 
       "lon": "52.3380919728735", 
       "name": "Amstelveenseweg, Amsterdam", 
       "id": "074901"
     }, 
     {
       "lat": "4.8573089172958", 
       "lon": "52.3380919728735", 
       "name": "Amstelveenseweg, Amsterdam", 
       "id": "074902"
     }, 
     {
       "lat": "4.85724722472001", 
       "lon": "52.3383433548049", 
       "name": "Amstelveenseweg, Amsterdam", 
       "id": "074931"
     }, 
     {
       "lat": "4.85724722472001", 
       "lon": "52.3383433548049", 
       "name": "Amstelveenseweg, Amsterdam", 
       "id": "074932"
     }, 
     {
       "lat": "4.85874927604203", 
       "lon": "52.3391230219462", 
       "name": "Amstelveenseweg, Amsterdam", 
       "id": "074952"
     }, 
     {
       "lat": "4.83862183531347", 
       "lon": "52.2841246456821", 
       "name": "Spinnerij, Amstelveen", 
       "id": "074963"
     }, 
     {
       "lat": "4.83787201861025", 
       "lon": "52.2843188981017", 
       "name": "Spinnerij, Amstelveen", 
       "id": "074973"
     }, 
     {
       "lat": "4.83276447370216", 
       "lon": "52.2825693800656", 
       "name": "Sacharovlaan, Amstelveen", 
       "id": "074983"
     }, 
     {
       "lat": "4.83231513757573", 
       "lon": "52.282171804221", 
       "name": "Sacharovlaan, Amstelveen", 
       "id": "074993"
     }, 
     {
       "lat": "4.83098656750543", 
       "lon": "52.2747415450464", 
       "name": "Westwijk, Amstelveen", 
       "id": "075003"
     }, 
     {
       "lat": "4.83052267497121", 
       "lon": "52.274343892999", 
       "name": "Westwijk, Amstelveen", 
       "id": "075013"
     }, 
     {
       "lat": "4.87214449343385", 
       "lon": "52.3114277354697", 
       "name": "Zonnestein, Amstelveen", 
       "id": "075442"
     }, 
     {
       "lat": "4.87227288277166", 
       "lon": "52.3079410151021", 
       "name": "Onderuit, Amstelveen", 
       "id": "075452"
     }, 
     {
       "lat": "4.87242880890461", 
       "lon": "52.3122019264518", 
       "name": "Zonnestein, Amstelveen", 
       "id": "075902"
     }, 
     {
       "lat": "4.87279490058309", 
       "lon": "52.3084466053027", 
       "name": "Onderuit, Amstelveen", 
       "id": "076232"
     }, 
     {
       "lat": "4.83252911496302", 
       "lon": "52.282640179371", 
       "name": "Sacharovlaan, Amstelveen", 
       "id": "077642"
     }, 
     {
       "lat": "4.8329459013685", 
       "lon": "52.2832982509762", 
       "name": "Sacharovlaan, Amstelveen", 
       "id": "077652"
     }, 
     {
       "lat": "4.84154646670957", 
       "lon": "52.2810643175619", 
       "name": "Zagerij, Amstelveen", 
       "id": "077912"
     }, 
     {
       "lat": "4.84165628939676", 
       "lon": "52.2840577948337", 
       "name": "Spinnerij, Amstelveen", 
       "id": "077922"
     }, 
     {
       "lat": "4.84124662869064", 
       "lon": "52.2840019765243", 
       "name": "Spinnerij, Amstelveen", 
       "id": "077932"
     }, 
     {
       "lat": "4.84605971514011", 
       "lon": "52.279880682572", 
       "name": "De Eindhoeve, Amstelveen", 
       "id": "078802"
     }, 
     {
       "lat": "4.84630892570989", 
       "lon": "52.2798728350831", 
       "name": "De Eindhoeve, Amstelveen", 
       "id": "078812"
     }, 
     {
       "lat": "4.85119523659903", 
       "lon": "52.2805422177462", 
       "name": "Middenhoven, Amstelveen", 
       "id": "078822"
     }, 
     {
       "lat": "4.85223810337177", 
       "lon": "52.2803402195301", 
       "name": "Middenhoven, Amstelveen", 
       "id": "078832"
     }, 
     {
       "lat": "4.85570098069055", 
       "lon": "52.2799603704196", 
       "name": "Praam, Amstelveen", 
       "id": "078842"
     }, 
     {
       "lat": "4.85537979549138", 
       "lon": "52.2798600592283", 
       "name": "Praam, Amstelveen", 
       "id": "078852"
     }, 
     {
       "lat": "4.84173541769248", 
       "lon": "52.2811910200907", 
       "name": "Zagerij, Amstelveen", 
       "id": "078872"
     }, 
     {
       "lat": "4.83051907586247", 
       "lon": "52.2746314894997", 
       "name": "Westwijk, Amstelveen", 
       "id": "079042"
     }, 
     {
       "lat": "4.82770985973918", 
       "lon": "52.277808938734", 
       "name": "B. von Suttnerlaan, Amstelveen", 
       "id": "079492"
     }, 
     {
       "lat": "4.93854919184537", 
       "lon": "52.3733451220261", 
       "name": "C. van Eesterenlaan, Amsterdam", 
       "id": "080112"
     }, 
     {
       "lat": "4.93885537687981", 
       "lon": "52.3735619861036", 
       "name": "C. van Eesterenlaan, Amsterdam", 
       "id": "080121"
     }, 
     {
       "lat": "4.93885537687981", 
       "lon": "52.3735619861036", 
       "name": "C. van Eesterenlaan, Amsterdam", 
       "id": "080122"
     }, 
     {
       "lat": "4.93734183612124", 
       "lon": "52.3765581305943", 
       "name": "Azartplein, Amsterdam", 
       "id": "080131"
     }, 
     {
       "lat": "4.93734183612124", 
       "lon": "52.3765581305943", 
       "name": "Azartplein, Amsterdam", 
       "id": "080132"
     }, 
     {
       "lat": "4.9373537866208", 
       "lon": "52.3768278062873", 
       "name": "Azartplein, Amsterdam", 
       "id": "080141"
     }, 
     {
       "lat": "4.9373537866208", 
       "lon": "52.3768278062873", 
       "name": "Azartplein, Amsterdam", 
       "id": "080142"
     }, 
     {
       "lat": "4.93786631215257", 
       "lon": "52.3769735549853", 
       "name": "Azartplein, Amsterdam", 
       "id": "080152"
     }, 
     {
       "lat": "4.93768808513578", 
       "lon": "52.3771706074346", 
       "name": "Azartplein, Amsterdam", 
       "id": "080162"
     }, 
     {
       "lat": "4.92079570995376", 
       "lon": "52.3691331960984", 
       "name": "Wittenburgergracht, Amsterdam", 
       "id": "080232"
     }, 
     {
       "lat": "4.91997121078496", 
       "lon": "52.3693456501568", 
       "name": "Wittenburgergracht, Amsterdam", 
       "id": "080242"
     }, 
     {
       "lat": "4.91596195570872", 
       "lon": "52.3707947563087", 
       "name": "Kattenburgerplein, Amsterdam", 
       "id": "080252"
     }, 
     {
       "lat": "4.9164051217427", 
       "lon": "52.3705448636752", 
       "name": "Kattenburgerplein, Amsterdam", 
       "id": "080262"
     }, 
     {
       "lat": "4.913568982554", 
       "lon": "52.3707492574589", 
       "name": "Kadijksplein, Amsterdam", 
       "id": "080272"
     }, 
     {
       "lat": "4.91327272692897", 
       "lon": "52.3709907399331", 
       "name": "Kadijksplein, Amsterdam", 
       "id": "080282"
     }, 
     {
       "lat": "4.90578253429158", 
       "lon": "52.3738275993321", 
       "name": "Prins Hendrikkade, Amsterdam", 
       "id": "080302"
     }, 
     {
       "lat": "4.90455661001639", 
       "lon": "52.3744787107603", 
       "name": "Prins Hendrikkade, Amsterdam", 
       "id": "080312"
     }, 
     {
       "lat": "4.91843777197719", 
       "lon": "52.3727279508948", 
       "name": "Kattenburgerstraat, Amsterdam", 
       "id": "080322"
     }, 
     {
       "lat": "4.9035594291656", 
       "lon": "52.3756969689716", 
       "name": "Prins Hendrikkade, Amsterdam", 
       "id": "080332"
     }, 
     {
       "lat": "4.9193439031527", 
       "lon": "52.3731359808919", 
       "name": "Kattenburgerstraat, Amsterdam", 
       "id": "080412"
     }, 
     {
       "lat": "4.91080716113837", 
       "lon": "52.3667656116424", 
       "name": "Plantage Kerklaan, Amsterdam", 
       "id": "080421"
     }, 
     {
       "lat": "4.91080716113837", 
       "lon": "52.3667656116424", 
       "name": "Plantage Kerklaan, Amsterdam", 
       "id": "080422"
     }, 
     {
       "lat": "4.91141162231133", 
       "lon": "52.3665343618546", 
       "name": "Plantage Kerklaan, Amsterdam", 
       "id": "080431"
     }, 
     {
       "lat": "4.91141162231133", 
       "lon": "52.3665343618546", 
       "name": "Plantage Kerklaan, Amsterdam", 
       "id": "080432"
     }, 
     {
       "lat": "4.95149330432609", 
       "lon": "52.3651607415057", 
       "name": "Flevopark, Amsterdam", 
       "id": "080441"
     }, 
     {
       "lat": "4.91553799472689", 
       "lon": "52.365094863602", 
       "name": "Plantage Badlaan, Amsterdam", 
       "id": "080451"
     }, 
     {
       "lat": "4.91553799472689", 
       "lon": "52.365094863602", 
       "name": "Plantage Badlaan, Amsterdam", 
       "id": "080452"
     }, 
     {
       "lat": "4.91528707451703", 
       "lon": "52.365219691637", 
       "name": "Plantage Badlaan, Amsterdam", 
       "id": "080461"
     }, 
     {
       "lat": "4.91528707451703", 
       "lon": "52.365219691637", 
       "name": "Plantage Badlaan, Amsterdam", 
       "id": "080462"
     }, 
     {
       "lat": "4.95084670541636", 
       "lon": "52.365221274048", 
       "name": "Flevopark, Amsterdam", 
       "id": "080471"
     }, 
     {
       "lat": "4.91916305569723", 
       "lon": "52.3638329952233", 
       "name": "Alexanderplein, Amsterdam", 
       "id": "080491"
     }, 
     {
       "lat": "4.91866836651289", 
       "lon": "52.3634086161305", 
       "name": "Alexanderplein, Amsterdam", 
       "id": "080501"
     }, 
     {
       "lat": "4.91365858855327", 
       "lon": "52.3623550965688", 
       "name": "K. 's-Gravesandestr., Amsterdam", 
       "id": "080511"
     }, 
     {
       "lat": "4.91550459029776", 
       "lon": "52.3627129868975", 
       "name": "K. 's-Gravesandestr., Amsterdam", 
       "id": "080521"
     }, 
     {
       "lat": "4.90655428502548", 
       "lon": "52.3608794435441", 
       "name": "Weesperplein, Amsterdam", 
       "id": "080531"
     }, 
     {
       "lat": "4.90941076512955", 
       "lon": "52.3614572329009", 
       "name": "Weesperplein, Amsterdam", 
       "id": "080541"
     }, 
     {
       "lat": "4.89833172983764", 
       "lon": "52.3636769071173", 
       "name": "Keizersgracht, Amsterdam", 
       "id": "080602"
     }, 
     {
       "lat": "4.898996374981", 
       "lon": "52.3619809701184", 
       "name": "Prinsengracht, Amsterdam", 
       "id": "080622"
     }, 
     {
       "lat": "4.89899005526971", 
       "lon": "52.3598868037515", 
       "name": "Frederiksplein, Amsterdam", 
       "id": "080642"
     }, 
     {
       "lat": "4.89751307578217", 
       "lon": "52.3593684028128", 
       "name": "Frederiksplein, Amsterdam", 
       "id": "080661"
     }, 
     {
       "lat": "4.89818773217307", 
       "lon": "52.3594251180209", 
       "name": "Frederiksplein, Amsterdam", 
       "id": "080671"
     }, 
     {
       "lat": "4.89159518916826", 
       "lon": "52.3595325175902", 
       "name": "Weteringcircuit, Amsterdam", 
       "id": "080721"
     }, 
     {
       "lat": "4.89227124376555", 
       "lon": "52.3594634441305", 
       "name": "Weteringcircuit, Amsterdam", 
       "id": "080731"
     }, 
     {
       "lat": "4.89111690776276", 
       "lon": "52.3602944715889", 
       "name": "Weteringcircuit, Amsterdam", 
       "id": "080761"
     }, 
     {
       "lat": "4.89075031953618", 
       "lon": "52.3589447747389", 
       "name": "Weteringcircuit, Amsterdam", 
       "id": "080781"
     }, 
     {
       "lat": "4.88690961098718", 
       "lon": "52.3610676865582", 
       "name": "Spiegelgracht, Amsterdam", 
       "id": "080801"
     }, 
     {
       "lat": "4.92193632063205", 
       "lon": "52.376579492592", 
       "name": "Jan Schaeferbrug, Amsterdam", 
       "id": "080832"
     }, 
     {
       "lat": "4.92170192497817", 
       "lon": "52.3765246452872", 
       "name": "Jan Schaeferbrug, Amsterdam", 
       "id": "080842"
     }, 
     {
       "lat": "4.89243902492035", 
       "lon": "52.364164727691", 
       "name": "Keizersgracht, Amsterdam", 
       "id": "080861"
     }, 
     {
       "lat": "4.89262546903188", 
       "lon": "52.3645609665787", 
       "name": "Keizersgracht, Amsterdam", 
       "id": "080871"
     }, 
     {
       "lat": "4.92547406749188", 
       "lon": "52.3597953314967", 
       "name": "Wijttenbachstraat, Amsterdam", 
       "id": "080941"
     }, 
     {
       "lat": "4.92547406749188", 
       "lon": "52.3597953314967", 
       "name": "Wijttenbachstraat, Amsterdam", 
       "id": "080942"
     }, 
     {
       "lat": "4.91969601805863", 
       "lon": "52.3634126786276", 
       "name": "Alexanderplein, Amsterdam", 
       "id": "080951"
     }, 
     {
       "lat": "4.91969601805863", 
       "lon": "52.3634126786276", 
       "name": "Alexanderplein, Amsterdam", 
       "id": "080952"
     }, 
     {
       "lat": "4.91931327637106", 
       "lon": "52.3635100314365", 
       "name": "Alexanderplein, Amsterdam", 
       "id": "080961"
     }, 
     {
       "lat": "4.91931327637106", 
       "lon": "52.3635100314365", 
       "name": "Alexanderplein, Amsterdam", 
       "id": "080962"
     }, 
     {
       "lat": "4.92411843862806", 
       "lon": "52.3616864438209", 
       "name": "1e v.Swindenstraat, Amsterdam", 
       "id": "080971"
     }, 
     {
       "lat": "4.92411843862806", 
       "lon": "52.3616864438209", 
       "name": "1e v.Swindenstraat, Amsterdam", 
       "id": "080972"
     }, 
     {
       "lat": "4.92386446484617", 
       "lon": "52.362107872513", 
       "name": "1e v.Swindenstraat, Amsterdam", 
       "id": "080981"
     }, 
     {
       "lat": "4.90927980999818", 
       "lon": "52.3572594374248", 
       "name": "Wibautstraat, Amsterdam", 
       "id": "090201"
     }, 
     {
       "lat": "4.92386446484617", 
       "lon": "52.362107872513", 
       "name": "1e v.Swindenstraat, Amsterdam", 
       "id": "080982"
     }, 
     {
       "lat": "4.92809710215022", 
       "lon": "52.3659261611225", 
       "name": "Pontanusstraat, Amsterdam", 
       "id": "081031"
     }, 
     {
       "lat": "4.92723088876732", 
       "lon": "52.3659227990366", 
       "name": "Pontanusstraat, Amsterdam", 
       "id": "081041"
     }, 
     {
       "lat": "4.93292983023024", 
       "lon": "52.3657021344575", 
       "name": "Zeeburgerdijk, Amsterdam", 
       "id": "081071"
     }, 
     {
       "lat": "4.93245781086929", 
       "lon": "52.3659160272088", 
       "name": "Zeeburgerdijk, Amsterdam", 
       "id": "081081"
     }, 
     {
       "lat": "4.9385550770585", 
       "lon": "52.3640518724686", 
       "name": "Javaplein, Amsterdam", 
       "id": "081101"
     }, 
     {
       "lat": "4.93824550331127", 
       "lon": "52.3641765267338", 
       "name": "Javaplein, Amsterdam", 
       "id": "081111"
     }, 
     {
       "lat": "4.93949565747333", 
       "lon": "52.3639565683305", 
       "name": "Javaplein, Amsterdam", 
       "id": "081132"
     }, 
     {
       "lat": "4.93955274913207", 
       "lon": "52.3641185627787", 
       "name": "Javaplein, Amsterdam", 
       "id": "081142"
     }, 
     {
       "lat": "4.93912924677626", 
       "lon": "52.3711633112779", 
       "name": "Borneolaan, Amsterdam", 
       "id": "081152"
     }, 
     {
       "lat": "4.94536133203826", 
       "lon": "52.3661266627737", 
       "name": "Kramatweg, Amsterdam", 
       "id": "081182"
     }, 
     {
       "lat": "4.94765061571834", 
       "lon": "52.364760067024", 
       "name": "Insulindeweg, Amsterdam", 
       "id": "081191"
     }, 
     {
       "lat": "4.94765061571834", 
       "lon": "52.364760067024", 
       "name": "Insulindeweg, Amsterdam", 
       "id": "081192"
     }, 
     {
       "lat": "4.94763664679827", 
       "lon": "52.3646881136207", 
       "name": "Insulindeweg, Amsterdam", 
       "id": "081201"
     }, 
     {
       "lat": "4.94763664679827", 
       "lon": "52.3646881136207", 
       "name": "Insulindeweg, Amsterdam", 
       "id": "081202"
     }, 
     {
       "lat": "4.94391718428224", 
       "lon": "52.3622475678215", 
       "name": "Soembawastraat, Amsterdam", 
       "id": "081211"
     }, 
     {
       "lat": "4.94391718428224", 
       "lon": "52.3622475678215", 
       "name": "Soembawastraat, Amsterdam", 
       "id": "081212"
     }, 
     {
       "lat": "4.94346308079393", 
       "lon": "52.3621470019787", 
       "name": "Soembawastraat, Amsterdam", 
       "id": "081241"
     }, 
     {
       "lat": "4.94346308079393", 
       "lon": "52.3621470019787", 
       "name": "Soembawastraat, Amsterdam", 
       "id": "081242"
     }, 
     {
       "lat": "4.93861024471521", 
       "lon": "52.3614995744023", 
       "name": "Molukkenstraat, Amsterdam", 
       "id": "081291"
     }, 
     {
       "lat": "4.93861024471521", 
       "lon": "52.3614995744023", 
       "name": "Molukkenstraat, Amsterdam", 
       "id": "081292"
     }, 
     {
       "lat": "4.94073636160719", 
       "lon": "52.3588382631728", 
       "name": "Valentijnkade, Amsterdam", 
       "id": "081312"
     }, 
     {
       "lat": "4.94079345126782", 
       "lon": "52.3590002571869", 
       "name": "Valentijnkade, Amsterdam", 
       "id": "081322"
     }, 
     {
       "lat": "4.96249194992829", 
       "lon": "52.3710966234371", 
       "name": "Zuiderzeeweg, Amsterdam", 
       "id": "081332"
     }, 
     {
       "lat": "4.96225417525144", 
       "lon": "52.3713923635723", 
       "name": "Zuiderzeeweg, Amsterdam", 
       "id": "081342"
     }, 
     {
       "lat": "4.91246197692978", 
       "lon": "52.3671677177671", 
       "name": "Plantage Kerklaan, Amsterdam", 
       "id": "081371"
     }, 
     {
       "lat": "4.90766053434115", 
       "lon": "52.361755738733", 
       "name": "Weesperplein, Amsterdam", 
       "id": "081472"
     }, 
     {
       "lat": "4.90144134149321", 
       "lon": "52.359914863014", 
       "name": "Oosteinde, Amsterdam", 
       "id": "081521"
     }, 
     {
       "lat": "4.90218891796129", 
       "lon": "52.3600167931911", 
       "name": "Oosteinde, Amsterdam", 
       "id": "081531"
     }, 
     {
       "lat": "4.90989832266094", 
       "lon": "52.3679932673134", 
       "name": "Plantage Parklaan, Amsterdam", 
       "id": "081701"
     }, 
     {
       "lat": "4.9075772135494", 
       "lon": "52.3613150028924", 
       "name": "Weesperplein, Amsterdam", 
       "id": "081722"
     }, 
     {
       "lat": "4.9209623920311", 
       "lon": "52.374229875413", 
       "name": "Marinierskade, Amsterdam", 
       "id": "081772"
     }, 
     {
       "lat": "4.92007166498052", 
       "lon": "52.3737500172394", 
       "name": "Marinierskade, Amsterdam", 
       "id": "081782"
     }, 
     {
       "lat": "4.91480538046149", 
       "lon": "52.3621978992235", 
       "name": "K. 's-Gravesandestr., Amsterdam", 
       "id": "081791"
     }, 
     {
       "lat": "4.92576974762063", 
       "lon": "52.3666541049968", 
       "name": "Zeeburgerstraat, Amsterdam", 
       "id": "081812"
     }, 
     {
       "lat": "4.92605141134358", 
       "lon": "52.3663945590622", 
       "name": "Zeeburgerstraat, Amsterdam", 
       "id": "081822"
     }, 
     {
       "lat": "4.93160508639854", 
       "lon": "52.3674586329674", 
       "name": "Het Funen, Amsterdam", 
       "id": "081832"
     }, 
     {
       "lat": "4.930870704263", 
       "lon": "52.3674827679022", 
       "name": "Het Funen, Amsterdam", 
       "id": "081842"
     }, 
     {
       "lat": "4.9401047503404", 
       "lon": "52.3661608556099", 
       "name": "Veelaan, Amsterdam", 
       "id": "081862"
     }, 
     {
       "lat": "4.94048620259983", 
       "lon": "52.3661892585276", 
       "name": "Veelaan, Amsterdam", 
       "id": "081872"
     }, 
     {
       "lat": "4.93934352589543", 
       "lon": "52.3615742522573", 
       "name": "Molukkenstraat, Amsterdam", 
       "id": "081901"
     }, 
     {
       "lat": "4.93934352589543", 
       "lon": "52.3615742522573", 
       "name": "Molukkenstraat, Amsterdam", 
       "id": "081902"
     }, 
     {
       "lat": "4.92498056221779", 
       "lon": "52.3677115753217", 
       "name": "Oostenburgergracht, Amsterdam", 
       "id": "081962"
     }, 
     {
       "lat": "4.92294802780835", 
       "lon": "52.3683147866242", 
       "name": "Oostenburgergracht, Amsterdam", 
       "id": "081972"
     }, 
     {
       "lat": "4.93567573466937", 
       "lon": "52.3685527498585", 
       "name": "Stadsdeel Zeeburg, Amsterdam", 
       "id": "082002"
     }, 
     {
       "lat": "4.93588165492262", 
       "lon": "52.3685175841887", 
       "name": "Stadsdeel Zeeburg, Amsterdam", 
       "id": "082012"
     }, 
     {
       "lat": "4.94530171016879", 
       "lon": "52.3662163171746", 
       "name": "Kramatweg, Amsterdam", 
       "id": "082032"
     }, 
     {
       "lat": "4.94601604451776", 
       "lon": "52.3682052604317", 
       "name": "Th.K .v. Lohuizenlaan, Amsterdam", 
       "id": "082042"
     }, 
     {
       "lat": "4.94285849203717", 
       "lon": "52.3770732815248", 
       "name": "Levantplein, Amsterdam", 
       "id": "082072"
     }, 
     {
       "lat": "4.94238811180501", 
       "lon": "52.3771164539448", 
       "name": "Levantplein, Amsterdam", 
       "id": "082082"
     }, 
     {
       "lat": "4.9460159217671", 
       "lon": "52.377076099385", 
       "name": "KNSM-laan, Amsterdam", 
       "id": "082092"
     }, 
     {
       "lat": "4.94617915874198", 
       "lon": "52.3680440897362", 
       "name": "Th.K .v. Lohuizenlaan, Amsterdam", 
       "id": "082142"
     }, 
     {
       "lat": "4.93861778388604", 
       "lon": "52.3709187071867", 
       "name": "Borneolaan, Amsterdam", 
       "id": "082152"
     }, 
     {
       "lat": "4.9383570317969", 
       "lon": "52.3705671992547", 
       "name": "Borneolaan, Amsterdam", 
       "id": "082162"
     }, 
     {
       "lat": "4.92308225621397", 
       "lon": "52.3793432078894", 
       "name": "Tosaristraat, Amsterdam", 
       "id": "082242"
     }, 
     {
       "lat": "4.92934184436671", 
       "lon": "52.3790440188221", 
       "name": "Majanggracht, Amsterdam", 
       "id": "082252"
     }, 
     {
       "lat": "4.93135760459305", 
       "lon": "52.3786833006323", 
       "name": "Majanggracht, Amsterdam", 
       "id": "082262"
     }, 
     {
       "lat": "4.92309543740312", 
       "lon": "52.3794870624177", 
       "name": "Tosaristraat, Amsterdam", 
       "id": "082292"
     }, 
     {
       "lat": "4.90955861771924", 
       "lon": "52.3722700444015", 
       "name": "IJ tunnel, Amsterdam", 
       "id": "082322"
     }, 
     {
       "lat": "4.93812226231628", 
       "lon": "52.3734513558321", 
       "name": "C. van Eesterenlaan, Amsterdam", 
       "id": "082331"
     }, 
     {
       "lat": "4.91316192664473", 
       "lon": "52.3772367441117", 
       "name": "Muziekgeb. Bimhuis, Amsterdam", 
       "id": "082341"
     }, 
     {
       "lat": "4.91289759118169", 
       "lon": "52.3772356856364", 
       "name": "Muziekgeb. Bimhuis, Amsterdam", 
       "id": "082351"
     }, 
     {
       "lat": "4.9220297098021", 
       "lon": "52.376076549099", 
       "name": "Kattenburgerstraat, Amsterdam", 
       "id": "082361"
     }, 
     {
       "lat": "4.92126533794285", 
       "lon": "52.3761454454175", 
       "name": "Kattenburgerstraat, Amsterdam", 
       "id": "082371"
     }, 
     {
       "lat": "4.93349898165207", 
       "lon": "52.3732180271421", 
       "name": "Rietlandpark, Amsterdam", 
       "id": "082381"
     }, 
     {
       "lat": "4.93413305613764", 
       "lon": "52.3729598121115", 
       "name": "Rietlandpark, Amsterdam", 
       "id": "082391"
     }, 
     {
       "lat": "4.96116052229936", 
       "lon": "52.3721254228264", 
       "name": "Zuiderzeeweg, Amsterdam", 
       "id": "082401"
     }, 
     {
       "lat": "4.96185255164786", 
       "lon": "52.3719301819214", 
       "name": "Zuiderzeeweg, Amsterdam", 
       "id": "082411"
     }, 
     {
       "lat": "4.98083463144866", 
       "lon": "52.3628024585628", 
       "name": "Steigereiland, Amsterdam", 
       "id": "082441"
     }, 
     {
       "lat": "4.98012691043594", 
       "lon": "52.363132571498", 
       "name": "Steigereiland, Amsterdam", 
       "id": "082451"
     }, 
     {
       "lat": "4.99104137999495", 
       "lon": "52.3574893815468", 
       "name": "Vennepluimstraat, Amsterdam", 
       "id": "082461"
     }, 
     {
       "lat": "4.99056980813694", 
       "lon": "52.3576945193178", 
       "name": "Vennepluimstraat, Amsterdam", 
       "id": "082471"
     }, 
     {
       "lat": "4.99546607088349", 
       "lon": "52.3551223689061", 
       "name": "Diemerparklaan, Amsterdam", 
       "id": "082481"
     }, 
     {
       "lat": "4.99499454462772", 
       "lon": "52.3553275244516", 
       "name": "Diemerparklaan, Amsterdam", 
       "id": "082491"
     }, 
     {
       "lat": "4.99991956600059", 
       "lon": "52.3527642727172", 
       "name": "Ruisrietstraat, Amsterdam", 
       "id": "082501"
     }, 
     {
       "lat": "4.9994186520501", 
       "lon": "52.3529783374256", 
       "name": "Ruisrietstraat, Amsterdam", 
       "id": "082511"
     }, 
     {
       "lat": "5.00432382945607", 
       "lon": "52.3509540987611", 
       "name": "IJburg, Amsterdam", 
       "id": "082521"
     }, 
     {
       "lat": "5.00469884205537", 
       "lon": "52.3517192646569", 
       "name": "IJburg, Amsterdam", 
       "id": "082531"
     }, 
     {
       "lat": "4.92421366240743", 
       "lon": "52.3666300548012", 
       "name": "Hoogte Kadijk, Amsterdam", 
       "id": "082541"
     }, 
     {
       "lat": "4.92482776951278", 
       "lon": "52.3668751225928", 
       "name": "Hoogte Kadijk, Amsterdam", 
       "id": "082551"
     }, 
     {
       "lat": "4.926515937401", 
       "lon": "52.3683197351253", 
       "name": "1e Coehoornstraat, Amsterdam", 
       "id": "082561"
     }, 
     {
       "lat": "4.92618067111378", 
       "lon": "52.3680847500102", 
       "name": "1e Coehoornstraat, Amsterdam", 
       "id": "082571"
     }, 
     {
       "lat": "4.92943423649428", 
       "lon": "52.3700926420927", 
       "name": "1e Leeghwaterstraat, Amsterdam", 
       "id": "082581"
     }, 
     {
       "lat": "4.93004703115087", 
       "lon": "52.3704724927283", 
       "name": "1e Leeghwaterstraat, Amsterdam", 
       "id": "082591"
     }, 
     {
       "lat": "4.93444169372956", 
       "lon": "52.3729340295851", 
       "name": "Rietlandpark, Amsterdam", 
       "id": "082601"
     }, 
     {
       "lat": "4.93480805833049", 
       "lon": "52.3730073313502", 
       "name": "Rietlandpark, Amsterdam", 
       "id": "082611"
     }, 
     {
       "lat": "4.93843067509731", 
       "lon": "52.3690934974961", 
       "name": "Cruquiusweg, Amsterdam", 
       "id": "082622"
     }, 
     {
       "lat": "4.93655567166315", 
       "lon": "52.3773280815656", 
       "name": "Azartplein, Amsterdam", 
       "id": "082641"
     }, 
     {
       "lat": "4.93863614132257", 
       "lon": "52.3691032637645", 
       "name": "Cruquiusweg, Amsterdam", 
       "id": "082652"
     }, 
     {
       "lat": "4.97993259619218", 
       "lon": "52.3635093857562", 
       "name": "Steigereiland, Amsterdam", 
       "id": "082682"
     }, 
     {
       "lat": "4.98145360133661", 
       "lon": "52.3625439387142", 
       "name": "Steigereiland, Amsterdam", 
       "id": "082692"
     }, 
     {
       "lat": "4.99472731735117", 
       "lon": "52.3556681708879", 
       "name": "Diemerparklaan, Amsterdam", 
       "id": "082702"
     }, 
     {
       "lat": "4.9957330513845", 
       "lon": "52.3548086830293", 
       "name": "Diemerparklaan, Amsterdam", 
       "id": "082712"
     }, 
     {
       "lat": "4.99139679937816", 
       "lon": "52.3571400506699", 
       "name": "Vennepluimstraat, Amsterdam", 
       "id": "082812"
     }, 
     {
       "lat": "4.99033213185685", 
       "lon": "52.3580082917294", 
       "name": "Vennepluimstraat, Amsterdam", 
       "id": "082822"
     }, 
     {
       "lat": "5.00018665753201", 
       "lon": "52.3524326017349", 
       "name": "Ruisrietstraat, Amsterdam", 
       "id": "082852"
     }, 
     {
       "lat": "4.99915147291224", 
       "lon": "52.3533189940596", 
       "name": "Ruisrietstraat, Amsterdam", 
       "id": "082862"
     }, 
     {
       "lat": "4.94670991717029", 
       "lon": "52.3722612890258", 
       "name": "R.J.H. Fortuynplein, Amsterdam", 
       "id": "082882"
     }, 
     {
       "lat": "4.94016416632964", 
       "lon": "52.3617211570796", 
       "name": "Molukkenstraat, Amsterdam", 
       "id": "082901"
     }, 
     {
       "lat": "4.94016416632964", 
       "lon": "52.3617211570796", 
       "name": "Molukkenstraat, Amsterdam", 
       "id": "082902"
     }, 
     {
       "lat": "4.94100012510828", 
       "lon": "52.3618052000167", 
       "name": "Molukkenstraat, Amsterdam", 
       "id": "082911"
     }, 
     {
       "lat": "4.94100012510828", 
       "lon": "52.3618052000167", 
       "name": "Molukkenstraat, Amsterdam", 
       "id": "082912"
     }, 
     {
       "lat": "4.9395231963535", 
       "lon": "52.3655924333164", 
       "name": "Zeeburgerdijk, Amsterdam", 
       "id": "082922"
     }, 
     {
       "lat": "4.9394664657061", 
       "lon": "52.3653944894886", 
       "name": "Zeeburgerdijk, Amsterdam", 
       "id": "082932"
     }, 
     {
       "lat": "4.91706917173936", 
       "lon": "52.3771624441278", 
       "name": "Pass.Term. A'dam, Amsterdam", 
       "id": "082941"
     }, 
     {
       "lat": "5.00764792075719", 
       "lon": "52.3518455968768", 
       "name": "P.Oosterhuisstraat, Amsterdam", 
       "id": "082992"
     }, 
     {
       "lat": "5.00733808764371", 
       "lon": "52.3520333444814", 
       "name": "P.Oosterhuisstraat, Amsterdam", 
       "id": "083002"
     }, 
     {
       "lat": "4.89364081358299", 
       "lon": "52.3419160899947", 
       "name": "Dintelstraat, Amsterdam", 
       "id": "090011"
     }, 
     {
       "lat": "4.89364081358299", 
       "lon": "52.3419160899947", 
       "name": "Dintelstraat, Amsterdam", 
       "id": "090012"
     }, 
     {
       "lat": "4.89289236092798", 
       "lon": "52.3419219540168", 
       "name": "Dintelstraat, Amsterdam", 
       "id": "090031"
     }, 
     {
       "lat": "4.89289236092798", 
       "lon": "52.3419219540168", 
       "name": "Dintelstraat, Amsterdam", 
       "id": "090032"
     }, 
     {
       "lat": "4.89216625514691", 
       "lon": "52.3399236348572", 
       "name": "Europaplein, Amsterdam", 
       "id": "090041"
     }, 
     {
       "lat": "4.89216625514691", 
       "lon": "52.3399236348572", 
       "name": "Europaplein, Amsterdam", 
       "id": "090042"
     }, 
     {
       "lat": "4.89227792805666", 
       "lon": "52.3404364046969", 
       "name": "Europaplein, Amsterdam", 
       "id": "090051"
     }, 
     {
       "lat": "4.89227792805666", 
       "lon": "52.3404364046969", 
       "name": "Europaplein, Amsterdam", 
       "id": "090052"
     }, 
     {
       "lat": "4.92840887600508", 
       "lon": "52.347134051615", 
       "name": "Maxwellstraat, Amsterdam", 
       "id": "090082"
     }, 
     {
       "lat": "4.91383289933626", 
       "lon": "52.3584011972716", 
       "name": "Camperstraat, Amsterdam", 
       "id": "090231"
     }, 
     {
       "lat": "4.91339329495169", 
       "lon": "52.3583275368226", 
       "name": "Camperstraat, Amsterdam", 
       "id": "090241"
     }, 
     {
       "lat": "4.90986570065856", 
       "lon": "52.3573786418138", 
       "name": "Wibautstraat, Amsterdam", 
       "id": "090271"
     }, 
     {
       "lat": "4.91810454910562", 
       "lon": "52.3486934785183", 
       "name": "Prins Bernhardplein, Amsterdam", 
       "id": "090302"
     }, 
     {
       "lat": "4.91779103360386", 
       "lon": "52.3491955488653", 
       "name": "Prins Bernhardplein, Amsterdam", 
       "id": "090312"
     }, 
     {
       "lat": "4.91916501439944", 
       "lon": "52.3469450675929", 
       "name": "Amstelstation, Amsterdam", 
       "id": "090321"
     }, 
     {
       "lat": "4.9191773207861", 
       "lon": "52.3471698097559", 
       "name": "Amstelstation, Amsterdam", 
       "id": "090331"
     }, 
     {
       "lat": "4.91950112569729", 
       "lon": "52.3470812123221", 
       "name": "Amstelstation, Amsterdam", 
       "id": "090342"
     }, 
     {
       "lat": "4.91921709382204", 
       "lon": "52.3461813155507", 
       "name": "Amstelstation, Amsterdam", 
       "id": "090372"
     }, 
     {
       "lat": "4.91909978830212", 
       "lon": "52.3461718639274", 
       "name": "Amstelstation, Amsterdam", 
       "id": "090382"
     }, 
     {
       "lat": "4.91893864734792", 
       "lon": "52.3461442632849", 
       "name": "Amstelstation, Amsterdam", 
       "id": "090392"
     }, 
     {
       "lat": "4.91901192767938", 
       "lon": "52.3461535409253", 
       "name": "Amstelstation, Amsterdam", 
       "id": "090412"
     }, 
     {
       "lat": "4.90538021266391", 
       "lon": "52.3459730039363", 
       "name": "Victorieplein, Amsterdam", 
       "id": "090471"
     }, 
     {
       "lat": "4.90510932910991", 
       "lon": "52.3465920555812", 
       "name": "Victorieplein, Amsterdam", 
       "id": "090481"
     }, 
     {
       "lat": "4.90510932910991", 
       "lon": "52.3465920555812", 
       "name": "Victorieplein, Amsterdam", 
       "id": "090482"
     }, 
     {
       "lat": "4.90569877217698", 
       "lon": "52.3463697613111", 
       "name": "Victorieplein, Amsterdam", 
       "id": "090491"
     }, 
     {
       "lat": "4.90569877217698", 
       "lon": "52.3463697613111", 
       "name": "Victorieplein, Amsterdam", 
       "id": "090492"
     }, 
     {
       "lat": "4.904987436997", 
       "lon": "52.3470049954602", 
       "name": "Victorieplein, Amsterdam", 
       "id": "090501"
     }, 
     {
       "lat": "4.904987436997", 
       "lon": "52.3470049954602", 
       "name": "Victorieplein, Amsterdam", 
       "id": "090502"
     }, 
     {
       "lat": "4.90653437571198", 
       "lon": "52.3464540475181", 
       "name": "Victorieplein, Amsterdam", 
       "id": "090511"
     }, 
     {
       "lat": "4.90653437571198", 
       "lon": "52.3464540475181", 
       "name": "Victorieplein, Amsterdam", 
       "id": "090512"
     }, 
     {
       "lat": "4.90643948105937", 
       "lon": "52.3430203410789", 
       "name": "Uiterwaardenstraat, Amsterdam", 
       "id": "090551"
     }, 
     {
       "lat": "4.90660478636107", 
       "lon": "52.3426615022779", 
       "name": "Uiterwaardenstraat, Amsterdam", 
       "id": "090561"
     }, 
     {
       "lat": "4.90462995089561", 
       "lon": "52.3407390739537", 
       "name": "Hunzestraat, Amsterdam", 
       "id": "090571"
     }, 
     {
       "lat": "4.90709767509909", 
       "lon": "52.3405064411951", 
       "name": "Pres. Kennedylaan, Amsterdam", 
       "id": "090581"
     }, 
     {
       "lat": "4.90103632357982", 
       "lon": "52.3446250529466", 
       "name": "Waalstraat, Amsterdam", 
       "id": "090601"
     }, 
     {
       "lat": "4.90103632357982", 
       "lon": "52.3446250529466", 
       "name": "Waalstraat, Amsterdam", 
       "id": "090602"
     }, 
     {
       "lat": "4.90059825615682", 
       "lon": "52.3444255220528", 
       "name": "Waalstraat, Amsterdam", 
       "id": "090611"
     }, 
     {
       "lat": "4.90059825615682", 
       "lon": "52.3444255220528", 
       "name": "Waalstraat, Amsterdam", 
       "id": "090612"
     }, 
     {
       "lat": "4.90131484380173", 
       "lon": "52.3446531599728", 
       "name": "Waalstraat, Amsterdam", 
       "id": "090632"
     }, 
     {
       "lat": "4.90173775674291", 
       "lon": "52.3408710494933", 
       "name": "Pres. Kennedylaan, Amsterdam", 
       "id": "090642"
     }, 
     {
       "lat": "4.90189827835702", 
       "lon": "52.3409525977015", 
       "name": "Pres. Kennedylaan, Amsterdam", 
       "id": "090652"
     }, 
     {
       "lat": "4.89635936932852", 
       "lon": "52.3428980745506", 
       "name": "Maasstraat, Amsterdam", 
       "id": "090681"
     }, 
     {
       "lat": "4.89635936932852", 
       "lon": "52.3428980745506", 
       "name": "Maasstraat, Amsterdam", 
       "id": "090682"
     }, 
     {
       "lat": "4.89684132525198", 
       "lon": "52.3431067909099", 
       "name": "Maasstraat, Amsterdam", 
       "id": "090691"
     }, 
     {
       "lat": "4.89684132525198", 
       "lon": "52.3431067909099", 
       "name": "Maasstraat, Amsterdam", 
       "id": "090692"
     }, 
     {
       "lat": "4.88951880614135", 
       "lon": "52.3470218518114", 
       "name": "Scheldestraat, Amsterdam", 
       "id": "090702"
     }, 
     {
       "lat": "4.88961710028342", 
       "lon": "52.3474177263894", 
       "name": "Scheldestraat, Amsterdam", 
       "id": "090712"
     }, 
     {
       "lat": "4.89056699385983", 
       "lon": "52.3438445879048", 
       "name": "Scheldeplein, Amsterdam", 
       "id": "090722"
     }, 
     {
       "lat": "4.89113255962118", 
       "lon": "52.3444491398419", 
       "name": "Scheldeplein, Amsterdam", 
       "id": "090732"
     }, 
     {
       "lat": "4.8911574142465", 
       "lon": "52.3474781184975", 
       "name": "Scheldestraat, Amsterdam", 
       "id": "090741"
     }, 
     {
       "lat": "4.89161476031786", 
       "lon": "52.3472643282492", 
       "name": "Scheldestraat, Amsterdam", 
       "id": "090751"
     }, 
     {
       "lat": "4.89476046996622", 
       "lon": "52.3468100949513", 
       "name": "Maasstraat, Amsterdam", 
       "id": "090781"
     }, 
     {
       "lat": "4.89544741676843", 
       "lon": "52.3470646082079", 
       "name": "Maasstraat, Amsterdam", 
       "id": "090791"
     }, 
     {
       "lat": "4.89973832674964", 
       "lon": "52.3465610687871", 
       "name": "Waalstraat, Amsterdam", 
       "id": "090821"
     }, 
     {
       "lat": "4.90032267042623", 
       "lon": "52.3468061433051", 
       "name": "Waalstraat, Amsterdam", 
       "id": "090831"
     }, 
     {
       "lat": "4.90432236701346", 
       "lon": "52.3487818578615", 
       "name": "Amstelkade, Amsterdam", 
       "id": "090861"
     }, 
     {
       "lat": "4.90432236701346", 
       "lon": "52.3487818578615", 
       "name": "Amstelkade, Amsterdam", 
       "id": "090862"
     }, 
     {
       "lat": "4.90406671444909", 
       "lon": "52.3493470425344", 
       "name": "Jozef Isra\u00eblskade, Amsterdam", 
       "id": "090881"
     }, 
     {
       "lat": "4.90406671444909", 
       "lon": "52.3493470425344", 
       "name": "Jozef Isra\u00eblskade, Amsterdam", 
       "id": "090882"
     }, 
     {
       "lat": "4.90330959306944", 
       "lon": "52.3514830325148", 
       "name": "Lutmastraat, Amsterdam", 
       "id": "090901"
     }, 
     {
       "lat": "4.90330959306944", 
       "lon": "52.3514830325148", 
       "name": "Lutmastraat, Amsterdam", 
       "id": "090902"
     }, 
     {
       "lat": "4.90312955115534", 
       "lon": "52.351841805987", 
       "name": "Lutmastraat, Amsterdam", 
       "id": "090911"
     }, 
     {
       "lat": "4.90312955115534", 
       "lon": "52.351841805987", 
       "name": "Lutmastraat, Amsterdam", 
       "id": "090912"
     }, 
     {
       "lat": "4.90142609029764", 
       "lon": "52.3546030509199", 
       "name": "Ceintuurbaan, Amsterdam", 
       "id": "090941"
     }, 
     {
       "lat": "4.90142609029764", 
       "lon": "52.3546030509199", 
       "name": "Ceintuurbaan, Amsterdam", 
       "id": "090942"
     }, 
     {
       "lat": "4.90105412465295", 
       "lon": "52.3550598984202", 
       "name": "Ceintuurbaan, Amsterdam", 
       "id": "090951"
     }, 
     {
       "lat": "4.90105412465295", 
       "lon": "52.3550598984202", 
       "name": "Ceintuurbaan, Amsterdam", 
       "id": "090952"
     }, 
     {
       "lat": "4.90162774441249", 
       "lon": "52.3549544000067", 
       "name": "Van Woustraat, Amsterdam", 
       "id": "090961"
     }, 
     {
       "lat": "4.90083809226003", 
       "lon": "52.3546815260652", 
       "name": "Van Woustraat, Amsterdam", 
       "id": "090971"
     }, 
     {
       "lat": "4.90475855926094", 
       "lon": "52.3559109133973", 
       "name": "Amsteldijk, Amsterdam", 
       "id": "090981"
     }, 
     {
       "lat": "4.90405596117244", 
       "lon": "52.3557282931791", 
       "name": "Amsteldijk, Amsterdam", 
       "id": "090991"
     }, 
     {
       "lat": "4.89918172798865", 
       "lon": "52.3584765205023", 
       "name": "Stadhouderskade, Amsterdam", 
       "id": "091001"
     }, 
     {
       "lat": "4.89923080547051", 
       "lon": "52.3580183485166", 
       "name": "Stadhouderskade, Amsterdam", 
       "id": "091011"
     }, 
     {
       "lat": "4.89923080547051", 
       "lon": "52.3580183485166", 
       "name": "Stadhouderskade, Amsterdam", 
       "id": "091012"
     }, 
     {
       "lat": "4.8894019706309", 
       "lon": "52.3548227277133", 
       "name": "Albert Cuypstraat, Amsterdam", 
       "id": "091041"
     }, 
     {
       "lat": "4.89040860490426", 
       "lon": "52.3553752090055", 
       "name": "Albert Cuypstraat, Amsterdam", 
       "id": "091071"
     }, 
     {
       "lat": "4.89423467414893", 
       "lon": "52.3531892079725", 
       "name": "2e v.d.Helststraat, Amsterdam", 
       "id": "091081"
     }, 
     {
       "lat": "4.89487908012488", 
       "lon": "52.3533177183546", 
       "name": "2e v.d.Helststraat, Amsterdam", 
       "id": "091091"
     }, 
     {
       "lat": "4.89153766318269", 
       "lon": "52.3528543862504", 
       "name": "Ferd. Bolstraat, Amsterdam", 
       "id": "091101"
     }, 
     {
       "lat": "4.89073182501031", 
       "lon": "52.3527251806262", 
       "name": "Ferd. Bolstraat, Amsterdam", 
       "id": "091111"
     }, 
     {
       "lat": "4.89123295724416", 
       "lon": "52.3525385387964", 
       "name": "Ceintuurbaan, Amsterdam", 
       "id": "091131"
     }, 
     {
       "lat": "4.88642191645812", 
       "lon": "52.3522486498575", 
       "name": "Ruysdaelkade, Amsterdam", 
       "id": "091151"
     }, 
     {
       "lat": "4.88708248211759", 
       "lon": "52.3522424549584", 
       "name": "Ruysdaelkade, Amsterdam", 
       "id": "091161"
     }, 
     {
       "lat": "4.89149609721461", 
       "lon": "52.3500050960286", 
       "name": "Cornelis Troostplein, Amsterdam", 
       "id": "091191"
     }, 
     {
       "lat": "4.89160838945848", 
       "lon": "52.3504639415185", 
       "name": "Cornelis Troostplein, Amsterdam", 
       "id": "091201"
     }, 
     {
       "lat": "4.89085065918636", 
       "lon": "52.3578486917015", 
       "name": "Stadhouderskade, Amsterdam", 
       "id": "091271"
     }, 
     {
       "lat": "4.89073815525347", 
       "lon": "52.3574078207888", 
       "name": "Stadhouderskade, Amsterdam", 
       "id": "091281"
     }, 
     {
       "lat": "4.91123824489183", 
       "lon": "52.3471111870487", 
       "name": "Amsteldijk, Amsterdam", 
       "id": "091391"
     }, 
     {
       "lat": "4.91123824489183", 
       "lon": "52.3471111870487", 
       "name": "Amsteldijk, Amsterdam", 
       "id": "091392"
     }, 
     {
       "lat": "4.91054917994989", 
       "lon": "52.3470454998523", 
       "name": "Amsteldijk, Amsterdam", 
       "id": "091401"
     }, 
     {
       "lat": "4.91054917994989", 
       "lon": "52.3470454998523", 
       "name": "Amsteldijk, Amsterdam", 
       "id": "091402"
     }, 
     {
       "lat": "4.8963980876001", 
       "lon": "52.3407231966217", 
       "name": "Maasstraat, Amsterdam", 
       "id": "091602"
     }, 
     {
       "lat": "4.89844053091889", 
       "lon": "52.3404710042927", 
       "name": "Maasstraat, Amsterdam", 
       "id": "091612"
     }, 
     {
       "lat": "4.90548761849925", 
       "lon": "52.3455420291264", 
       "name": "Victorieplein, Amsterdam", 
       "id": "091701"
     }, 
     {
       "lat": "4.92275662478745", 
       "lon": "52.3515339722783", 
       "name": "James Wattstraat, Amsterdam", 
       "id": "091752"
     }, 
     {
       "lat": "4.92328893537647", 
       "lon": "52.351158575061", 
       "name": "James Wattstraat, Amsterdam", 
       "id": "091762"
     }, 
     {
       "lat": "4.92075901027424", 
       "lon": "52.3530720068354", 
       "name": "Krugerplein, Amsterdam", 
       "id": "091772"
     }, 
     {
       "lat": "4.92080408110692", 
       "lon": "52.3529733194166", 
       "name": "Krugerplein, Amsterdam", 
       "id": "091782"
     }, 
     {
       "lat": "4.92826536899776", 
       "lon": "52.3482389865223", 
       "name": "Maxwellstraat, Amsterdam", 
       "id": "091792"
     }, 
     {
       "lat": "4.90979673707833", 
       "lon": "52.3583310626612", 
       "name": "Wibautstraat, Amsterdam", 
       "id": "091802"
     }, 
     {
       "lat": "4.91039905948244", 
       "lon": "52.3569224172031", 
       "name": "Wibautstraat, Amsterdam", 
       "id": "091812"
     }, 
     {
       "lat": "4.89148064484135", 
       "lon": "52.3579591843642", 
       "name": "Ferd. Bolstraat, Amsterdam", 
       "id": "091842"
     }, 
     {
       "lat": "4.91956285673849", 
       "lon": "52.3467938485579", 
       "name": "Amstelstation, Amsterdam", 
       "id": "091862"
     }, 
     {
       "lat": "4.89239043508399", 
       "lon": "52.3579899539336", 
       "name": "Ferd. Bolstraat, Amsterdam", 
       "id": "091882"
     }, 
     {
       "lat": "4.90113280643658", 
       "lon": "52.3773587444742", 
       "name": "Centraal Station, Amsterdam", 
       "id": "095003"
     }, 
     {
       "lat": "4.90129507569771", 
       "lon": "52.3719308393899", 
       "name": "Nieuwmarkt, Amsterdam", 
       "id": "095023"
     }, 
     {
       "lat": "4.90123624313242", 
       "lon": "52.3719395856453", 
       "name": "Nieuwmarkt, Amsterdam", 
       "id": "095033"
     }, 
     {
       "lat": "4.90305221751043", 
       "lon": "52.3670037851142", 
       "name": "Waterlooplein, Amsterdam", 
       "id": "095083"
     }, 
     {
       "lat": "4.90297910230453", 
       "lon": "52.3669765229655", 
       "name": "Waterlooplein, Amsterdam", 
       "id": "095093"
     }, 
     {
       "lat": "4.90803326481588", 
       "lon": "52.3612269724434", 
       "name": "Weesperplein, Amsterdam", 
       "id": "095103"
     }, 
     {
       "lat": "4.90787207613834", 
       "lon": "52.3611993567541", 
       "name": "Weesperplein, Amsterdam", 
       "id": "095113"
     }, 
     {
       "lat": "4.91223222712798", 
       "lon": "52.3543413208514", 
       "name": "Wibautstraat, Amsterdam", 
       "id": "095123"
     }, 
     {
       "lat": "4.91202731635464", 
       "lon": "52.3542865720849", 
       "name": "Wibautstraat, Amsterdam", 
       "id": "095133"
     }, 
     {
       "lat": "4.91757016224507", 
       "lon": "52.3464893631328", 
       "name": "Amstelstation, Amsterdam", 
       "id": "095143"
     }, 
     {
       "lat": "4.91751165188786", 
       "lon": "52.3464711554724", 
       "name": "Amstelstation, Amsterdam", 
       "id": "095153"
     }, 
     {
       "lat": "4.93017174045436", 
       "lon": "52.3298574301876", 
       "name": "Van der Madeweg, Amsterdam", 
       "id": "095163"
     }, 
     {
       "lat": "4.93048396218972", 
       "lon": "52.3294541862914", 
       "name": "Van der Madeweg, Amsterdam", 
       "id": "095173"
     }, 
     {
       "lat": "4.92089441012556", 
       "lon": "52.3401841214516", 
       "name": "Spaklerweg, Amsterdam", 
       "id": "095183"
     }, 
     {
       "lat": "4.92102948722203", 
       "lon": "52.3398970455559", 
       "name": "Spaklerweg, Amsterdam", 
       "id": "095193"
     }, 
     {
       "lat": "4.94136011381112", 
       "lon": "52.3186654046915", 
       "name": "Strandvliet, Amsterdam", 
       "id": "095203"
     }, 
     {
       "lat": "4.94152558673165", 
       "lon": "52.3182525903546", 
       "name": "Strandvliet, Amsterdam", 
       "id": "095213"
     }, 
     {
       "lat": "4.94668633230944", 
       "lon": "52.3125197390148", 
       "name": "Station Bijlmer ArenA, Amsterdam", 
       "id": "095223"
     }, 
     {
       "lat": "4.94713212542179", 
       "lon": "52.3119282043308", 
       "name": "Station Bijlmer ArenA, Amsterdam", 
       "id": "095233"
     }, 
     {
       "lat": "4.95207892983004", 
       "lon": "52.3069313173479", 
       "name": "Bullewijk, Amsterdam", 
       "id": "095243"
     }, 
     {
       "lat": "4.9523331983989", 
       "lon": "52.3064199482009", 
       "name": "Bullewijk, Amsterdam", 
       "id": "095253"
     }, 
     {
       "lat": "4.95987347521127", 
       "lon": "52.2984033509566", 
       "name": "Station Holendrecht , Amsterdam", 
       "id": "095263"
     }, 
     {
       "lat": "4.96021642318177", 
       "lon": "52.2978024067053", 
       "name": "Station Holendrecht , Amsterdam", 
       "id": "095273"
     }, 
     {
       "lat": "4.97363594851544", 
       "lon": "52.2955851671529", 
       "name": "Reigersbos, Amsterdam", 
       "id": "095283"
     }, 
     {
       "lat": "4.97473466264144", 
       "lon": "52.2956609064839", 
       "name": "Reigersbos, Amsterdam", 
       "id": "095293"
     }, 
     {
       "lat": "4.98847817119039", 
       "lon": "52.2963911109912", 
       "name": "Gein, Amsterdam", 
       "id": "095303"
     }, 
     {
       "lat": "4.98952006457006", 
       "lon": "52.2962687897895", 
       "name": "Gein, Amsterdam", 
       "id": "095313"
     }, 
     {
       "lat": "4.9460466873874", 
       "lon": "52.326727025842", 
       "name": "Venserpolder, Amsterdam", 
       "id": "095403"
     }, 
     {
       "lat": "4.9466474781203", 
       "lon": "52.326792178612", 
       "name": "Venserpolder, Amsterdam", 
       "id": "095413"
     }, 
     {
       "lat": "4.95610523378944", 
       "lon": "52.3302153972622", 
       "name": "Station Diemen-Zuid, Diemen", 
       "id": "095423"
     }, 
     {
       "lat": "4.95713011960388", 
       "lon": "52.3304258448407", 
       "name": "Station Diemen-Zuid, Diemen", 
       "id": "095433"
     }, 
     {
       "lat": "4.96654910453298", 
       "lon": "52.3288149451397", 
       "name": "Verrijn Stuartweg, Amsterdam", 
       "id": "095443"
     }, 
     {
       "lat": "4.96693407985885", 
       "lon": "52.328438827678", 
       "name": "Verrijn Stuartweg, Amsterdam", 
       "id": "095453"
     }, 
     {
       "lat": "4.97285820291116", 
       "lon": "52.3239838210791", 
       "name": "Station Ganzenhoef, Amsterdam", 
       "id": "095463"
     }, 
     {
       "lat": "4.9732311789875", 
       "lon": "52.3233110451238", 
       "name": "Station Ganzenhoef, Amsterdam", 
       "id": "095473"
     }, 
     {
       "lat": "4.97940728599009", 
       "lon": "52.3168253568968", 
       "name": "Station Kraaiennest, Amsterdam", 
       "id": "095483"
     }, 
     {
       "lat": "4.97963188408208", 
       "lon": "52.3163228161606", 
       "name": "Station Kraaiennest, Amsterdam", 
       "id": "095493"
     }, 
     {
       "lat": "4.98448844097638", 
       "lon": "52.3112254091089", 
       "name": "Gaasperplas, Amsterdam", 
       "id": "095503"
     }, 
     {
       "lat": "4.93678167619282", 
       "lon": "52.3232498038937", 
       "name": "Station Duivendrecht, Amsterdam", 
       "id": "095513"
     }, 
     {
       "lat": "4.93626174540996", 
       "lon": "52.3238949430165", 
       "name": "Station Duivendrecht, Amsterdam", 
       "id": "095523"
     }, 
     {
       "lat": "4.98468289364841", 
       "lon": "52.3108036457424", 
       "name": "Gaasperplas, Amsterdam", 
       "id": "095553"
     }, 
     {
       "lat": "4.87509592311023", 
       "lon": "52.3390780484161", 
       "name": "Station Zuid, Amsterdam", 
       "id": "095623"
     }, 
     {
       "lat": "4.91815099732771", 
       "lon": "52.3317966875527", 
       "name": "Overamstel, Amsterdam", 
       "id": "095633"
     }, 
     {
       "lat": "4.93033264445325", 
       "lon": "52.3299029903742", 
       "name": "Van der Madeweg, Amsterdam", 
       "id": "095643"
     }, 
     {
       "lat": "4.93032315211116", 
       "lon": "52.3293996389002", 
       "name": "Van der Madeweg, Amsterdam", 
       "id": "095653"
     }, 
     {
       "lat": "4.92085378927318", 
       "lon": "52.3398604023343", 
       "name": "Spaklerweg, Amsterdam", 
       "id": "095663"
     }, 
     {
       "lat": "4.92106992068049", 
       "lon": "52.340238739371", 
       "name": "Spaklerweg, Amsterdam", 
       "id": "095673"
     }, 
     {
       "lat": "4.88641604698754", 
       "lon": "52.3930887916206", 
       "name": "Tasmanstraat, Amsterdam", 
       "id": "099004"
     }, 
     {
       "lat": "4.89647918827232", 
       "lon": "52.3957732854693", 
       "name": "Distelweg, Amsterdam", 
       "id": "099014"
     }, 
     {
       "lat": "4.89173466352324", 
       "lon": "52.4009394156602", 
       "name": "NDSM-werf, Amsterdam", 
       "id": "099024"
     }, 
     {
       "lat": "4.89925927065623", 
       "lon": "52.3807933258056", 
       "name": "Centraal Station, Amsterdam", 
       "id": "099034"
     }, 
     {
       "lat": "4.89958415153466", 
       "lon": "52.3806328855685", 
       "name": "Centraal Station, Amsterdam", 
       "id": "099054"
     }, 
     {
       "lat": "4.90317935177115", 
       "lon": "52.3822654183957", 
       "name": "Buiksloterweg, Amsterdam", 
       "id": "099064"
     }, 
     {
       "lat": "4.89865217536774", 
       "lon": "52.381240207298", 
       "name": "Centraal Station, Amsterdam", 
       "id": "099104"
     }, 
     {
       "lat": "4.90828125957146", 
       "lon": "52.3817738629192", 
       "name": "IJplein, Amsterdam", 
       "id": "099114"
     }, 
     {
       "lat": "4.90439914867475", 
       "lon": "52.3687079627544", 
       "name": "Waterlooplein, Amsterdam", 
       "id": "990032"
     }, 
     {
       "lat": "4.90476660124589", 
       "lon": "52.3686735097285", 
       "name": "Waterlooplein, Amsterdam", 
       "id": "990042"
     }, 
     {
       "lat": "4.4320591231704", 
       "lon": "52.2406511745327", 
       "name": "noordwijk, Noordwijk, Pick\u00e9plein", 
       "id": "54660260"
     }, 
     {
       "lat": "4.43086677016796", 
       "lon": "52.2416302449416", 
       "name": "noordwijk, Noordwijk, Pick\u00e9plein", 
       "id": "54660270"
     }
   ]


HALTES = sorted(HALTES, key=lambda halte: halte['name'])

def index(request):
    halteids = request.GET.get('halteids', '').split(',')
    
    return render_to_response('govi/index.html', {
        'halteids': halteids
    }, context_instance=RequestContext(request))
    
def pick(request):
    return render_to_response('govi/pick.html', {
        'haltes': HALTES
    }, context_instance=RequestContext(request))
    
def halte(request, halteid):
    dris = urllib2.urlopen('http://cache.govi.openov.nl/kv55/%s' % halteid).read()
    dom = parseString(dris)
    
    trips = dom.getElementsByTagName('Trip')
    
    now = datetime.datetime.now()
    
    destination = ''
    minutesUntil = []
    
    for trip in trips:
        destination = trip.getElementsByTagName('DestinationName')[0].childNodes[0].data
        expected = trip.getElementsByTagName('ExpectedDepartureTime')[0].childNodes[0].data
        
        expectedTime = datetime.datetime(now.year, now.month, now.day, int(expected.split(':')[0]), int(expected.split(':')[1]), int(expected.split(':')[2]))
        
        minutesUntil.append((expectedTime - now).seconds / 60)
        
    return HttpResponse(json.dumps({'destination': destination, 'minutes': minutesUntil}), mimetype='application/json')