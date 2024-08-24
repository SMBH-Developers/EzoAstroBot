import asyncio

from pyrogram import errors
from loguru import logger

from src.config import client
from src.enum import Status
from src.models import db
from src.funnels import funnels
from .types import MyGeneratedMessage


payed_triggers = ["@EveOfficials", "Oжидaть", "oжидaть", "@EvasAstro", '@EveHarmonis',
                  "прекраснo", "Прекраснo",
                  "@EveMyOfficials", "AstroMentorr", "MyHarmonis", "RunesMentor", "MyTaroMento",
                  "My_Mentorr", "Matrix_Harmony", "AstroHarmonis", "Harmony_Mentor",
                  "YourAstrologys", "MentorGuides", "HarmonyMentorr", "@HarmonyGuides", "MySpiritualMentor",
                  "@YourAstroMentor", "Your_soul_traveler", "Duhovnysputnik", "LoveHarmonis", "@Adel_Numero", "@YourMentorLife", "@Your_Soul_Astrology"]


class Dispatcher:

    @logger.catch
    async def sending_message(self, id_: int, day: int, step: int, message: MyGeneratedMessage) -> bool:

        with logger.catch():
            try:
                if 'audio' == message.content_type_to_send:
                    with message.others_kwargs['audio'].open('rb') as audio_to_send:
                        message.others_kwargs['audio'] = audio_to_send
                        await client.send_audio(id_, **message.others_kwargs)
                        
                elif 'document' == message.content_type_to_send:
                    with message.others_kwargs['document'].open('rb') as document_to_send:
                        message.others_kwargs['document'] = document_to_send
                        await client.send_document(id_, **message.others_kwargs)
                        
                elif 'video_note' == message.content_type_to_send:
                    with message.others_kwargs['video_note'].open('rb') as video_note_to_send:
                        message.others_kwargs['video_note'] = video_note_to_send
                        await client.send_video_note(id_, **message.others_kwargs)

                elif 'photo' == message.content_type_to_send:
                    with message.others_kwargs['photo'].open('rb') as video_note_to_send:
                        message.others_kwargs['photo'] = video_note_to_send
                        await client.send_photo(id_, **message.others_kwargs)

                elif 'video' == message.content_type_to_send:
                    with message.others_kwargs['video'].open('rb') as video_to_send:
                        message.others_kwargs['video'] = video_to_send
                        await client.send_video(id_, **message.others_kwargs)
                elif 'voice' == message.content_type_to_send:
                    with message.others_kwargs['voice'].open('rb') as voice_to_send:
                        message.others_kwargs['voice'] = voice_to_send
                        await client.send_voice(id_, **message.others_kwargs)
                
                else:
                    await client.send_message(id_, **message.others_kwargs)
                sent_msg = True
                await db.update_last_message_at_bot(id_)
                logger.info(f"MESSAGE | Отправил сообщение User - {id_}")
                if message.last_message:
                    await db.set_day_message(id_, day+1, 0)
                else:
                    await db.set_day_message(id_, day=day, message=step+1)
                await client.read_chat_history(id_)

            except errors.exceptions.FloodWait as e:
                logger.error(f'MESSAGE FLOOD | {id_} got flood wait {e.value}')
                await asyncio.sleep(e.value + 2)

            except errors.PeerFlood:
                logger.error(f'PeerFlood | [{id_}]. Setting status: <{Status.PEER_FLOOD.value}>')
                await db.set_status(id_, Status.PEER_FLOOD.value)

            except errors.PeerIdInvalid:
                logger.error(f'PeerIdInvalid | [{id_}]. Setting status: <{Status.ID_INVALID.value}>')
                await db.set_status(id_, Status.ID_INVALID.value)

            except Exception as ex:
                logger.error(f'MESSAGE ERROR| {id_} got error. Ex: {ex}')
            else:
                await asyncio.sleep(1.5)
                return sent_msg

    @logger.catch
    async def check_triggers(self, id_: int, specific_trigger: list = None, day: int = None, step: int = None) -> bool:
        try:
            async for message in client.get_chat_history(id_):
                if message.text and message.outgoing:
                    text = message.text.lower()
                    for trigger in payed_triggers:
                        if trigger.lower() in text:
                            await db.set_status(id_, Status.PAYED.value)
                            logger.success(f'TRIGGER | User - {id_} is ready to pay. Trigger - {trigger}')
                            return True

                    if specific_trigger is not None:
                        for trigger in specific_trigger:
                            if trigger.lower() in text:
                                logger.info(f'TRIGGER | User - {id_} have specific trigger: {specific_trigger} on {day}-{step}')
                                await db.set_day_message(id_, day=day+1, message=step)
                                return True

        except errors.PeerIdInvalid:
            await db.set_status(id_, Status.ID_INVALID.value)
            return True
        return False

    @logger.catch
    async def dispatch_funnel_day(self, id_: int):
        funnel = await db.get_user_funnel(id_)
        day, step = (await db.get_user_step(id_)).split('-')

        # noinspection PyPep8Naming
        FunnelConfig = funnels[funnel]

        if int(day) in FunnelConfig.skip_days:
            logger.info(f"SYSTEM | Пропустил день - {int(day) + 1} для пользователя {id_}")
            return await db.set_day_message(id_, day=int(day) + 1, message=0)
        message_day: list[MyGeneratedMessage] = (await FunnelConfig.get_message(id_, day))[int(step):]

        for message in message_day:
            day, step = (await db.get_user_step(id_)).split('-')
            if not await message.filter(id_, day, step):
                return

            elif not await self.check_triggers(id_=id_, specific_trigger=message.trigger_from_our_account_to_cancel, day=int(day), step=int(step)):
                await asyncio.sleep(message.seconds_wait_before_sending)
                if await self.sending_message(id_=id_, day=int(day), step=int(step), message=message):
                    logger.success(f'SYSTEM | Удалось отправить сообщние User - {id_}, day {day} step {step}')
                else:
                    return
            else:
                return

