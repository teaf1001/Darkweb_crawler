import requests
from bs4 import BeautifulSoup
import re
import time
import math
import dd
import db

proxies = {
    'http': 'socks5h://127.0.0.1:9150',
    'https': 'socks5h://127.0.0.1:9150'
}

if __name__=='__main__':
    topics = ['porn','pornography','internet','prostitution','striptease','erotica','sex','pornographic','porno','movie','sexual arousal','playboy','pornographic film','smut','creation','masturbation','obscenity','eroticism','nudity','animation','erotic literature','photograph','voyeurism','pornographic film actor','movies','blue movie','andy warhol','religion','hollywood','erotic','united states','golden age of porn','video','fetish','raunchy','prostitutes','topless','pimp','novel','youtube','racy','sleazy','nude','gay','pornographer','pedophile','story','model','morality','censorship','moral','production','consumption','multimedia','common law','drawing','painting','better','goodish','amelioration','caregiver','dsl','goodly','honorably','sed','ameliorate','magick','saintliness','graphics','athenaeus','softcore','prehistory','impressionism','pornhub','redtube','olympia','youporn','nongood','teen','goodo','pompeii','betterish','exhibitionists','human sexual activity','hack','cut','hacker','horse','drudge','nag','foul','chop','plug','whoop','jade','cab','taxi','taxicab','equus caballus','ward-heeler','machine politician','literary hack','hack writer','hack on','cut up','political hack','edit','saddle horse','axe','steal','fleet','manage','grapple','machine','car','automobile','auto','deal','mount','rugby','programme','cope','program','contend','cough','politico','politician','ax','pol','writer','author','hoops','basketball','tool','motorcar','minicab','plodder','slogger','redact','rugger','dobbin','hosting','hostess','emcee','legion','hospitality','master of ceremonies','guest','compere','server','innkeeper','horde','army','entertain','multitude','entertainer','recipient','organization','receiver','venue','presenter','series','boniface','bread','junket','feast','banquet','ringmaster','sullivan','medicine','being','computing','organism','adult','computer','victualler','concourse','throng','organisation','padrone','toastmaster','patron','hosts','hosting','hosted','breadstuff','symposiarch','grownup','quizmaster','victualer','sabaoth','friendly','conference','event','upcoming','weekend','bitcoin','blockchain','currency','bitcoin network','cryptography','node','satoshi nakamoto','open-source software','cryptocurrency wallet','cryptocurrency exchange','cryptocurrency','public-key cryptography','ethereum','qt','central bank','distributed ledger','university of cambridge','nobel memorial prize in economic sciences','gavin andresen','silk road','youtube','segwit','kraken','ledger','financial crimes enforcement network','forth','double-spending','lightning network','bitcoin cash','unit of account','digital signature','cryptographic hash','megabyte','winklevoss twins','synchronization','bitcoin xt','baidu','proof-of-concept','cve','leveldb','nyse','micropayment','openssl','andreas antonopoulos','bitinstant','unicode','broadcasting','banknote','malleability','counterfeit','fake','false','phony','bogus','forgery','spurious','sham','pseudo','imitation','scam','fraud','fictitious','forged','phoney','identity theft','unreal','insincere','handbags','forge','imitative','illegal','base','bastard','fictive','mock','synthetic','assumed','pretended','pinchbeck','bad','ostensible','fraudulent','unauthentic','inauthentic','ostensive','pirated','contraband','smuggled','put on','confiscated','heroin','printing','forgeries','stolen','cocaine','illicit','counterfeiters','banknotes','methamphetamine','theft','jewelry','illegally','marijuana','coins','narcotics','jewellery','knockoffs','united states secret service','sale','currency','document','clothing','shoes','falsely','falsification','pharmaceutical','artificial','falsity','manufacture','falseness','deception','mendacious','watch','deceit','falsify','imposture','dishonesty','untruthful','falsehood','mendacity','charlatan','untruth','electronics','feign','delusive','untrue','mislead','deceitful','deceiver','deceive','delude','imposter','deceptive','software','delusion','hoax','misrepresentation','trickery','fib','swindle','duplicity','dupe','liar','impostor','misrepresent','lig','art','lie','defraud','cozen','chicanery','perjure','bilk','humbug','subterfuge','forger','bask','ingenuine','cheat','deceptively','toys','re-create','jugglery','pretense','trickster','guile','bamboozle','faithlessness','swindler','falsifier','belie','fallacious','movies','insincerity','dissimulate','perjury','amuser','unfaithful','hocus','cheater','gullible','trick','fraudulence','shlenter','fraudster','logos','blench','mendaciously','beguile','treacherous','embezzlement','counterfeiting','waylay','fakery','flimflam','whopper','brands','pretender','deceptiveness','laity','layoff','fibbery','prevarication','hoodwink','falsifiable','decipiency','mislie','unlying','blag','perjurer','adulterous','counterfeits','falsificationism','gull','rort','fool','dupery','importing','forlay','finagler','copying','overreach','chouse','prevaricate','forlie','imported','befool','fakes','import','hornswoggle','blesh','undeceive','belirt','drug','medicine','dope','psychoactive drug','medication','dose','stimulant','narcotic','injectable','pharmaceutical','pharmacy','analgesic','prescription','prescription drug','alcohol','drop','absorption','antisyphilitic','abortifacient','medicate','addiction','medicament','aspirin','tobacco','cannabis','fertility drug','narcotize','pharmaceutical drug','smoking','magic bullet','generic','antiviral','pharmacist','preventive medicine','physician','benzodiazepine','do drugs','anticonvulsant','antidrug','generic drug','antiemetic','probenecid','antidepressant','antibiotic','illegal','cocaine','marijuana','psychoactive substance','opiate','narcotics','heroin','amphetamine','methamphetamine','drug class','pills','medicines','chemical structure','mechanism of action','caffeine','vaccine','steroids','mode of action','cancer','anatomical therapeutic chemical classification system','atc code','biopharmaceutics classification system','hallucinogen','drug addiction','recreational drug use','single convention on narcotic drugs','who','over-the-counter drug','ingestion','substance','druggist','pharmacology','antihistamine','organism','codeine','anticholinergic','antibacterial','anticoagulant','biomedicine','chronic','immunology','prodrug','paregoric','food','apc','oncology','therapeutic','rheumatology','gastroenterology','anesthesiology','placebo','radiotherapy','insufflation','hypnotic','agent','relaxant','arsenical','pharmacopoeia','diuretic','botanical','overdose','orally','agonist','anaphylaxis','antagonist','anesthetic','trip','anaesthetic','excitant','soporific','poison','base','use','inject','snort','nephrology','drugs','purgative','palliative','neurology','nonspecific','panacea','therapy','pcp','clinician','laxative','urology','penicillin','curative','nostrum','remedy','medical','virology','dermatology','pediatrics','catatonic','psychiatry','gynecology','medic','nondrug','peptic','insulin','sedation','paracetamol','refractory','dispensary','pharmaceutic','neurologist','allopurinol','tiamulin','antidiabetic','acyclovir','opium','disulfiram','pentylenetetrazol','antispasmodic','carminative','gemfibrozil','antidiarrheal','decongestant','antiprotozoal','expectorant','md','splint','premedication','antitussive','pharmacon','physostigmine','psychotic','isoproterenol','medicinal','isosorbide','amrinone','antiarrhythmic','potentiation','perception','immunosuppressant','fever','clofibrate','medicative','vermifuge','antipyretic','sucralfate','antihypertensive','psychomedicine','anticholinesterase','mood','neurotropic','postdrug','parenteral','premedical','neuropsychiatry','clonic','azathioprine','aesculapian','venesect','traumatology','nonprescription','urinalysis','vermicide','penicillamine','proctology','consciousness','lorfan','anaesthetize','anaesthetise','free-base','anesthetize','uninjectable','habituate','narcotise','potentiate','aborticide','synergist','suppressant','dilator','feosol','fergon','o.d.','intoxicant','trental','levallorphan','pentoxifylline','mydriatic','myotic','miotic','anesthetise','podiatry','papaverine','hematinic','leechcraft','counterirritant','ethanol','ethnomedicine','suppository','mfm','pseudomedical','iatrophysics','polychrest','nonmedical','noninvasive','antidiuretic','infection','depressant','nosology','wonderdrug','pulmonology','bronchodilator','panpharmacon','nicotine','nanomedicine','trafficking','achromia','vasoconstrictor','oxytocic','phytomedicine','succedaneum','unguent','traffickers','digitalize','cases','zymosis','mercurialist','rubefacient','otology','treatment','hiv','tylenol','medications','aids','linked','smuggling','weapon','sword','gun','missile','spear','firearm','ammunition','artillery','projectile','rifle','pistol','bomb','bow','weaponry','arm','arms','knife','munition','cannon','guns','shotgun','tool','gunpowder','rocket','weapon system','world war ii','military','hunting','instrument','pike','bronze age','firearms','tank','war','machine gun','animal','fire ship','warfare','warhead','rock','armor','weapons','explosive','intercontinental ballistic missile','biological warfare','device','enemy','deterrent','sidearm','machine','caliber','firing','element','type','threat','target','dangerous','vehicle','warship','army','fire','weapon of mass destruction','ammo','power','armour','siege weapon','technology during world war i','injury','crime','club','teeth','axe','claw','tusk','knuckles','flamethrower','slasher','sling','lance','shaft','blade','brand','steel','hatchet','tomahawk','wmd','persuasion','suasion','stone','self-defense','hominids','bc','obsidian','neolithic','copper','metal','cyberweapon','knucks','w.m.d.','fortifications','catapult','spoke','chariot','china','cavalry','assault','handgun','europe','capable','explosives','trireme','possessing','arsenal','bombs','missiles','lethal','capability','revolver','knights','conventional','carry','nuclear','battery','ballistic','infantry','using','mobile','transportable','moving','changeful','changeable','telephone','smartphone','movable','motile','computer','cellular','portable','alabama','al','ala.','camellia state','heart of dixie','motorola','fluid','wandering','roving','peregrine','nomadic','network','radio','mobile river','ambulatory','maneuverable','transferable','moveable','airborne','floating','mechanized','waterborne','motorized','ambulant','versatile','perambulating','unsettled','seaborne','raisable','rangy','rotatable','manoeuvrable','transferrable','transplantable','raiseable','wireless','broadband','digital','cellphone','internet','online','multimedia','iphone','laptop','mobile phone','cellular phone','cellular telephone','river','port','metropolis','city','sculpture','racy','mechanised','urban','phones','operating','provider','pcs','hardware','devices','handset','networks','gsm','phone','users','software','handsets','pc','computers','networking','servers','equipment','systems','satellite','electronic','cable','telephony','services','communications','providers','handheld','server','mobility','electronics','customers','carriers','subscribers','service','telecommunications','web','operators','technology','access','operator','integrated','micro','messaging']
    handle = db.DB_Handler()

    for topic in topics:
        result = [0, 0]
        new_url = 0
        new_domain = 0
        parse_format = 'http://cnkj6nippubgycuj.onion/search?query={}&page={}'.format(topic, 1)
        res = requests.get(parse_format, proxies=proxies, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        num_of_page = math.ceil(int(re.findall("\d+", soup.p.text)[0]) / 25)

        for page in range(num_of_page):
            parse_format = 'http://cnkj6nippubgycuj.onion/search?query={}&page={}'.format(topic, page+1)
            res = requests.get(parse_format, proxies=proxies, timeout=10)
            result = dd.get_url(res, handle)
            new_domain += result[0]
            new_url += result[1]

        print("topic : {}\t new domain : {}\t new url : {}".format(topic, new_domain, new_url))





